import os
import json
import time
import threading
import vosk
import rclpy
import psutil
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor

from sobits_interfaces.action import SpeechRecognition
from ament_index_python.packages import get_package_share_directory
from .audio_utils import AudioSystem, AudioPlayer, AudioStorage

class VoskSR(Node):
    def __init__(self):
        super().__init__('vosk_node')
        self.GREEN, self.YELLOW, self.RED, self.ENDC = '\033[92m', '\033[93m', '\033[31m', '\033[0m'

        self.declare_parameter('model', "vosk-model-small-en-us-0.15")
        self.declare_parameter('use_echo_cancel', False)
        self.declare_parameter('noise_suppression', False)
        self.declare_parameter('analog_gain_control', False)
        self.declare_parameter('digital_gain_control', False)
        self.declare_parameter('mic_volume', "100%")

        model_name = self.get_parameter('model').value
        self.model_path = os.path.join(os.path.expanduser("~/.vosk_models"), model_name)

        self.sound_folder_path = os.path.join(get_package_share_directory('sobits_interfaces'), 'mp3')
        self.save_dir = os.path.join(get_package_share_directory('speech_recognition_vosk'), 'sound_file')

        self.audio_sys = AudioSystem(
            self.get_logger(), 
            use_echo_cancel=self.get_parameter('use_echo_cancel').value,
            noise_suppression=self.get_parameter('noise_suppression').value,
            analog_gain=self.get_parameter('analog_gain_control').value,
            digital_gain=self.get_parameter('digital_gain_control').value,
            mic_volume=self.get_parameter('mic_volume').value
        )
        self.player = AudioPlayer(self.get_logger(), self.sound_folder_path)
        self.storage = AudioStorage(self.get_logger(), self.save_dir)

        if not os.path.exists(self.model_path):
            self.get_logger().fatal(f"{self.RED}[MODEL NOT FOUND] {self.model_path}{self.ENDC}")
            return
        
        self.model = vosk.Model(self.model_path)
        self.get_logger().info(f"{self.GREEN}Vosk Model Loaded. [{self.get_resources()}]{self.ENDC}")

        self._callback_group = ReentrantCallbackGroup()
        self.server = ActionServer(
            self, SpeechRecognition, "speech_recognition",
            execute_callback=self.execute_callback,
            callback_group=self._callback_group,
            goal_callback=lambda g: GoalResponse.ACCEPT,
            cancel_callback=lambda g: CancelResponse.ACCEPT)
        
        self.get_logger().info(f"{self.YELLOW}Vosk Server READY{self.ENDC}")

    def get_resources(self):
        mem = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
        return f"Mem: {mem:.1f}MB"

    def execute_callback(self, goal_handle):
        container = {"text": "", "current_view": "", "done": False}
        stop_event = threading.Event()
        last_published_text = ""

        thread = threading.Thread(
            target=self._recognition_worker,
            args=(goal_handle, container, stop_event),
            daemon=True
        )
        thread.start()

        fb_period = 1.0 / float(goal_handle.request.feedback_rate)

        try:
            while not container["done"]:
                if goal_handle.is_cancel_requested:
                    stop_event.set()
                    goal_handle.canceled()
                    self.get_logger().info(f"{self.YELLOW}Action Canceled.{self.ENDC}")
                    return SpeechRecognition.Result()

                current_text = container["current_view"]
                if current_text and current_text != last_published_text:
                    new_part = current_text[len(last_published_text):].lstrip()
                    if new_part:
                        fb = SpeechRecognition.Feedback()
                        fb.addition_text = new_part
                        goal_handle.publish_feedback(fb)
                        last_published_text = current_text
                
                time.sleep(fb_period)
        finally:
            stop_event.set()
            self.audio_sys.stop()
            thread.join(timeout=1.0)

        result = SpeechRecognition.Result()
        result.result_text = container["text"] if container["text"] else "No speech recognized."
        
        self.get_logger().info(f"{self.GREEN}Succeeded: {result.result_text}{self.ENDC}")
        goal_handle.succeed()
        return result

    def _recognition_worker(self, goal_handle, container, stop_event):
        confirmed = []
        audio_started = False
        absolute_start_time = time.time() 
        detection_start_time = None

        try:
            self.audio_sys.start_recording(chunk_size=3200)
            self.storage.start_write_session("output.wav")

            if not goal_handle.request.silent_mode:
                self.player.play('start_sound.mp3')
            
            rec = vosk.KaldiRecognizer(self.model, 16000)

            while rclpy.ok() and not stop_event.is_set():
                now = time.time()

                if audio_started and (now - detection_start_time) > goal_handle.request.timeout_sec:
                    self.get_logger().info(f"{self.YELLOW}Recording timeout reached.{self.ENDC}")
                    break
                
                if not audio_started and (now - absolute_start_time) > (goal_handle.request.timeout_sec + 5.0):
                    self.get_logger().info(f"{self.RED}No audio detected. Force stopping.{self.ENDC}")
                    break

                data = self.audio_sys.read(timeout=0.01)
                if data is None:
                    continue
                
                if not audio_started:
                    audio_started = True
                    detection_start_time = time.time()
                    self.get_logger().info(f"{self.GREEN}Audio stream detected.{self.ENDC}")

                self.storage.write_chunk(data)
                raw_bytes = data.tobytes()
                partial = ""
                if rec.AcceptWaveform(raw_bytes):
                    res_dict = json.loads(rec.Result())
                    text = res_dict.get("text", "").strip()
                    if text: confirmed.append(text)
                else:
                    partial = json.loads(rec.PartialResult()).get("partial", "").strip()

                container["current_view"] = " ".join(confirmed + ([partial] if partial else [])).strip()

            final_res = json.loads(rec.FinalResult()).get("text", "").strip()
            if final_res: confirmed.append(final_res)

            if not goal_handle.request.silent_mode:
                self.player.play('end_sound.mp3')

            container["text"] = " ".join(confirmed).strip()

        except Exception as e:
            self.get_logger().error(f"Worker Thread Error: {e}")
        finally:
            self.storage.close_write_session()
            container["done"] = True

def main(args=None):
    try:
        rclpy.init(args=args)
        node = VoskSR()
        executor = MultiThreadedExecutor()
        try:
            rclpy.spin(node, executor=executor)
        finally:
            node.audio_sys.stop() 
            node.destroy_node()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()