"""Lo que se escucha en un video, palabra por palabra (faster-whisper).

    python3 -I scripts/tts/oir.py <video> <en|es>  -> JSON [{w, s, e}] en stdout
"""
import json, subprocess, sys

import numpy as np
from faster_whisper import WhisperModel

raw = subprocess.run(['ffmpeg', '-v', 'quiet', '-i', sys.argv[1], '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
audio = np.frombuffer(raw, np.float32)
modelo = WhisperModel('base.en' if sys.argv[2] == 'en' else 'small', device='cpu', compute_type='int8')
segs, _ = modelo.transcribe(audio, word_timestamps=True, language=sys.argv[2])
print(json.dumps([{'w': w.word.strip(), 's': round(w.start, 2), 'e': round(w.end, 2)} for s in segs for w in s.words], ensure_ascii=False))
