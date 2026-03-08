import os
import json
import vosk
import wave
from .base_engine import BaseEngine

class VoskEngine(BaseEngine):
    def __init__(self, node):
        super().__init__(node)

        self.is_streamable = True
        self.use_external_vad = False
        
        if not hasattr(self, 'model'):
            self._load_model()

        self.node.declare_parameter('vosk_grammar', "")
        self.grammar = self.node.get_parameter('vosk_grammar').value
        
        self.recognizer = None
        self.node.get_logger().info(f"[Vosk] Engine Ready. (Streamable: {self.is_streamable}, ExtVAD: {self.use_external_vad})")

    def _load_model(self):
        self.node.declare_parameter('model', "vosk-model-small-en-us-0.15")
        model_name = self.node.get_parameter('model').value
        model_path = os.path.join(os.path.expanduser("~/.vosk_models"), model_name)

        if not os.path.exists(model_path):
            self.node.get_logger().error(f"Vosk model not found at {model_path}")
            raise RuntimeError(f"Vosk model not found: {model_path}")

        self.node.get_logger().info(f"[Vosk] Loading model: {model_path}")
        self.model = vosk.Model(model_path)

    def init_stream(self):
        if self.grammar:
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000, self.grammar)
        else:
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.node.get_logger().info("[Vosk] Stream Initialized.")

    def put_chunk(self, chunk_np):
        if self.recognizer is None: return ""
        raw_bytes = chunk_np.tobytes()
        if self.recognizer.AcceptWaveform(raw_bytes):
            res = json.loads(self.recognizer.Result())
            return res.get("text", "").strip()
        return ""

    def transcribe(self, audio_path):
        if not os.path.exists(audio_path): return ""
        
        with wave.open(audio_path, "rb") as wf:
            tmp_rec = vosk.KaldiRecognizer(self.model, wf.getframerate())
            final_text_list = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0: break
                if tmp_rec.AcceptWaveform(data):
                    res = json.loads(tmp_rec.Result())
                    t = res.get("text", "").strip()
                    if t: final_text_list.append(t)
            
            res_final = json.loads(tmp_rec.FinalResult())
            t_final = res_final.get("text", "").strip()
            if t_final: final_text_list.append(t_final)
            
        return " ".join(final_text_list).strip()