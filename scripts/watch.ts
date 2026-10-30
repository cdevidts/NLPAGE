/**
 * Revisar un render como lo vería una persona: qué se ve y qué se ESCUCHA en
 * cada segundo (técnica de Videos-Next-Layer: los frames sueltos no muestran si
 * el sonido corresponde a la imagen ni si el subtítulo es lo que se dice).
 *
 *   npm run watch -- renders/<slug>.mp4 [--idioma es]
 *
 * Deja en out/watch/<nombre>/:
 *   - HOJA.jpg   un frame por segundo, numerado: ábrela con Read.
 *   - GUION.md   segundo a segundo, lo que whisper oye, el nivel y los silencios;
 *                arriba, loudness integrado y pico (meta: -14 LUFS, -1 dBTP).
 */
import fs from 'node:fs';
import path from 'node:path';
import {sh} from './lib/comun';

export const revisar = async (video: string, idioma: 'en' | 'es') => {
  const nombre = path.basename(video).replace(/\.\w+$/, '');
  const dir = path.join('out', 'watch', nombre);
  fs.rmSync(dir, {recursive: true, force: true});
  fs.mkdirSync(dir, {recursive: true});
  const dur = Number(sh('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video], {silencio: true}));
  const n = Math.ceil(dur);
  const cols = 8;
  const filas = Math.ceil(n / cols);
  sh('ffmpeg', [
    '-y', '-v', 'error', '-i', video,
    '-vf', `fps=1,scale=240:-2,drawtext=text='%{eif\\:n\\:d}s':x=8:y=8:fontsize=28:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=${cols}x${filas}:padding=4:color=white`,
    '-frames:v', '1', path.join(dir, 'HOJA.jpg'),
  ]);

  const tieneAudio = sh('ffprobe', ['-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', video], {silencio: true}).trim() !== '';
  const lineas: string[] = [`# ${nombre}`, '', `Duración: ${dur.toFixed(2)} s`];
  if (tieneAudio) {
    const r = sh('bash', ['-c', `ffmpeg -nostats -i "${video}" -af ebur128=peak=true -f null - 2>&1 | tail -12; ffmpeg -nostats -i "${video}" -af silencedetect=n=-40dB:d=0.4 -f null - 2>&1 | grep silence_ || true`], {silencio: true});
    const I = /I:\s+(-?[\d.]+) LUFS/.exec(r)?.[1];
    const TP = /Peak:\s+(-?[\d.]+) dBFS/.exec(r)?.[1];
    lineas.push(`Loudness: ${I ?? '?'} LUFS integrado, pico ${TP ?? '?'} dBTP (meta -14 / -1)`);
    const silencios = [...r.matchAll(/silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)/g)].map((m) => `${Number(m[1]).toFixed(1)}–${Number(m[2]).toFixed(1)} s`);
    lineas.push(`Silencios bajo -40 dB (≥0,4 s): ${silencios.length ? silencios.join(', ') : 'ninguno'}`);
    const oido = JSON.parse(sh('python3', ['-I', 'scripts/tts/oir.py', video, idioma], {silencio: true})) as Array<{w: string; s: number}>;
    lineas.push('', '| s | se escucha |', '|---|---|');
    for (let t = 0; t < n; t++) {
      const dicho = oido.filter((w) => w.s >= t && w.s < t + 1).map((w) => w.w).join(' ');
      lineas.push(`| ${t} | ${dicho || '·'} |`);
    }
  } else {
    lineas.push('Sin pista de audio (esperado en el video de Etsy).');
  }
  fs.writeFileSync(path.join(dir, 'GUION.md'), `${lineas.join('\n')}\n`);
  console.log(`✓ revisión: ${dir}/HOJA.jpg y ${dir}/GUION.md`);
  return dir;
};

if (process.argv[1] && path.basename(process.argv[1]).startsWith('watch')) {
  const video = process.argv[2];
  if (!video) throw new Error('Uso: npm run watch -- <video.mp4> [--idioma es]');
  const i = process.argv.indexOf('--idioma');
  await revisar(video, (i > 0 ? process.argv[i + 1] : 'en') as 'en' | 'es');
}
