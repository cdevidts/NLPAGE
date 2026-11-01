"""Tiempos de cada palabra de una voz en off, con el texto que se le dio al TTS.

    python3 -I scripts/tts/palabras.py <wav> <en|es> <texto>  -> JSON en stdout

faster-whisper escucha la voz y da tiempos por palabra; se emparejan con las
palabras del guion (difflib) y se devuelven las del GUION, no las de whisper:
el subtítulo dice lo que se escribió y suena, con el tiempo en que suena. Las
que whisper no oyó se interpolan entre sus vecinas por largo.
"""
import difflib, json, re, subprocess, sys

import numpy as np
from faster_whisper import WhisperModel

wav, idioma, texto = sys.argv[1], sys.argv[2], sys.argv[3]
raw = subprocess.run(['ffmpeg', '-v', 'quiet', '-i', wav, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
audio = np.frombuffer(raw, np.float32)
dur = len(audio) / 16000
modelo = WhisperModel('base.en' if idioma == 'en' else 'small', device='cpu', compute_type='int8')
# Sin initial_prompt: con el guion como pista whisper "oye" lo que espera y la
# compuerta deja pasar voces mal pronunciadas (pasó con "2013" en Piper).
segs, _ = modelo.transcribe(audio, word_timestamps=True, language=idioma)
oidas = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]

NUM = {
    'en': 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split(),
    'es': 'cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete dieciocho diecinueve veinte'.split(),
}[idioma]
DECENAS = 'twenty thirty forty fifty sixty seventy eighty ninety'.split()


def en_letras(n):
    """Inglés sin espacios ni guiones, como queda el guion tras norm: 54 -> fiftyfour, 1989 -> nineteeneightynine."""
    if n <= 20:
        return NUM[n]
    if n < 100:
        return DECENAS[n // 10 - 2] + (NUM[n % 10] if n % 10 else '')
    if 1100 <= n <= 2099 and n % 100:  # años: "nineteen eighty-nine", "twenty twenty-six"
        return en_letras(n // 100) + ('oh' + NUM[n % 100] if n % 100 < 10 else en_letras(n % 100))
    return str(n)


# Whisper escribe "1 a 6" o "1989" donde el guion dice "uno a seis" o "nineteen eighty-nine": se comparan en letras.
def norm(s):
    w = re.sub(r'[^\w]', '', s.lower())
    if not w.isdigit():
        return w
    n = int(w)
    return en_letras(n) if idioma == 'en' else (NUM[n] if n <= 20 else w)


guion = texto.split()
a = [norm(w) for w in guion]
b = [norm(w[0]) for w in oidas]
t = [None] * len(guion)
for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
    for k in range(blk.size):
        _, s, e = oidas[blk.b + k]
        t[blk.a + k] = [s, e]

# Interpolar los huecos entre vecinos conocidos, repartiendo por largo.
i = 0
while i < len(t):
    if t[i] is not None:
        i += 1
        continue
    j = i
    while j < len(t) and t[j] is None:
        j += 1
    ini = t[i - 1][1] if i > 0 else 0.0
    fin = t[j][0] if j < len(t) else dur
    largos = [max(len(guion[k]), 2) for k in range(i, j)]
    tot = sum(largos)
    acc = ini
    for k, l in zip(range(i, j), largos):
        d = (fin - ini) * l / tot
        t[k] = [acc, acc + d]
        acc += d
    i = j

oidas_txt = ' '.join(w[0] for w in oidas)
# Parecido por letras, no por palabras: whisper parte y junta distinto
# ("Do Re Mi note names" -> "do -remy notenames") sin que la voz esté mal.
similitud = difflib.SequenceMatcher(None, ''.join(a), ''.join(b), autojunk=False).ratio()
print(json.dumps({
    'palabras': [{'w': w, 's': round(s, 3), 'e': round(e, 3)} for w, (s, e) in zip(guion, t)],
    'oido': oidas_txt,
    'coinciden': sum(1 for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks() for _ in range(blk.size)),
    'total': len(guion),
    'similitud': round(similitud, 3),
    'dur': round(dur, 3),
}, ensure_ascii=False))
