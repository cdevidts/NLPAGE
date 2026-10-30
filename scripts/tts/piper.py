"""Voz en español con Piper (local, gratis, sin cuenta).

    python3 -I scripts/tts/piper.py <modelo.onnx> <salida.wav> <velocidad> <texto>
"""
import sys, wave
from piper import PiperVoice
from piper.config import SynthesisConfig

modelo, salida, velocidad, texto = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
voz = PiperVoice.load(modelo)
with wave.open(salida, 'wb') as w:
    # length_scale > 1 = más lento; velocidad 1.1 = 10 % más rápido.
    voz.synthesize_wav(texto, w, syn_config=SynthesisConfig(length_scale=1 / velocidad))
