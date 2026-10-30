/**
 * Voz, música, efectos e íconos. Todo gratis y sin cuenta:
 *   - Voz EN: Kokoro-82M (Apache 2.0) vía kokoro-js, modelo desde Hugging Face.
 *   - Voz ES: Piper es_MX-claude-high (dataset Apache 2.0), local.
 *   - Voz opcional "gemini:<Voz>" (ES/EN): Gemini TTS, free tier de la API; pide GEMINI_API_KEY
 *     (docs/gemini/README.md). El estilo va en plan.vozEstilo.
 *   - Tiempos de palabra: faster-whisper (MIT), local.
 *   - Música: Kevin MacLeod / incompetech.com, CC BY 4.0 (crédito en la descripción).
 *   - Efectos: catálogo medido de Mixkit (licencia Mixkit, sin atribución), heredado de Videos-Next-Layer.
 *   - Íconos: Iconify (sets MIT/Apache/CC BY, ver SETS).
 */
import fs from 'node:fs';
import path from 'node:path';
import {bajar, duracion, hash, sh} from './comun';
import type {Palabra, SfxRef} from '../../src/lib/types';

const CACHE = '.cache';

// --- Voz -------------------------------------------------------------------

let kokoro: unknown = null;

export const VOZ_DEFAULT = {en: 'af_heart', es: 'es_MX-claude-high'} as const;

/** Genera (o reusa) la voz de una línea. Devuelve el wav en .cache/voz/. */
export const voz = async (texto: string, idioma: 'en' | 'es', nombre?: string, velocidad = 1, estilo?: string) => {
  const v = nombre ?? VOZ_DEFAULT[idioma];
  const destino = path.join(CACHE, 'voz', `${hash(`${v}|${velocidad}|${estilo ? `${estilo}|` : ''}${texto}`)}.wav`);
  if (fs.existsSync(destino)) return destino;
  fs.mkdirSync(path.dirname(destino), {recursive: true});
  if (v.startsWith('gemini:')) {
    // Gemini no tiene parámetro de velocidad: se ajusta después con atempo.
    const crudo = destino.replace(/\.wav$/, '.gemini.wav');
    sh('python3', ['-I', 'scripts/gemini/gemini.py', 'voz', '--voz', v.slice(7), '--texto', texto, '--salida', crudo, ...(estilo ? ['--estilo', estilo] : [])], {silencio: true});
    sh('ffmpeg', ['-y', '-v', 'error', '-i', crudo, '-filter:a', `atempo=${velocidad}`, destino], {silencio: true});
  } else if (idioma === 'en') {
    const {KokoroTTS} = await import('kokoro-js');
    kokoro ??= await KokoroTTS.from_pretrained('onnx-community/Kokoro-82M-v1.0-ONNX', {dtype: 'q8', device: 'cpu'});
    const audio = await (kokoro as InstanceType<typeof KokoroTTS>).generate(texto, {voice: v as 'af_heart', speed: velocidad});
    await audio.save(destino);
  } else {
    sh('python3', ['-I', 'scripts/tts/piper.py', path.join(CACHE, 'piper', `${v}.onnx`), destino, String(velocidad), texto], {silencio: true});
  }
  return destino;
};

/** Palabras del guion con el tiempo en que suenan (faster-whisper + alineación). */
export const palabras = (wav: string, idioma: 'en' | 'es', texto: string) => {
  const cache = wav.replace(/\.wav$/, '.palabras.json');
  if (fs.existsSync(cache)) return JSON.parse(fs.readFileSync(cache, 'utf8')) as {palabras: Palabra[]; oido: string; coinciden: number; total: number; similitud: number};
  const out = sh('python3', ['-I', 'scripts/tts/palabras.py', wav, idioma, texto], {silencio: true});
  fs.writeFileSync(cache, out);
  return JSON.parse(out) as {palabras: Palabra[]; oido: string; coinciden: number; total: number; similitud: number};
};

// --- Música ------------------------------------------------------------------

export type Pieza = {title: string; filename: string; length: string; bpm: string; feel: string; description: string; instruments: string};

export const catalogoMusica = async (): Promise<Pieza[]> => {
  const archivo = path.join(CACHE, 'incompetech.json');
  await bajar('https://incompetech.com/music/royalty-free/pieces.json', archivo);
  return JSON.parse(fs.readFileSync(archivo, 'utf8')) as Pieza[];
};

export const musica = async (titulo: string) => {
  const pieza = (await catalogoMusica()).find((p) => p.title.toLowerCase() === titulo.toLowerCase());
  if (!pieza) throw new Error(`No existe "${titulo}" en incompetech (npm run musica -- --buscar ...)`);
  const archivo = `assets/music/${pieza.filename.replace(/[^\w.-]+/g, '_')}`;
  await bajar(`https://incompetech.com/music/royalty-free/mp3-royaltyfree/${encodeURIComponent(pieza.filename)}`, path.join('public', archivo));
  return {
    src: archivo,
    credito: `Music: "${pieza.title}" by Kevin MacLeod (incompetech.com). Licensed under Creative Commons: By Attribution 4.0 License, http://creativecommons.org/licenses/by/4.0/`,
  };
};

// --- Efectos -----------------------------------------------------------------

type Efecto = {id: string; rol: string; archivo: string; url: string; apto?: boolean; picoSeg?: number; nivelDb?: number; brilloHz?: number; nombre: string};

const catalogo = () => JSON.parse(fs.readFileSync('public/assets/sfx/catalog.json', 'utf8')) as Efecto[];

/** Nivel de referencia: cada efecto se lleva a -20 dB "activos" (medidos). */
const ref = async (e: Efecto): Promise<SfxRef> => {
  await bajar(e.url, path.join('public', e.archivo));
  return {id: e.id, src: e.archivo, picoSeg: e.picoSeg ?? 0, gananciaDb: Math.max(-12, Math.min(12, -20 - (e.nivelDb ?? -20)))};
};

/**
 * Whooshes graves (mitad baja del brillo) y pops, de Mixkit, rotando. La
 * semilla (el slug) hace que cada video tenga su propia mezcla.
 */
export const efectosBase = async (semilla: string) => {
  const c = catalogo().filter((e) => e.apto && e.id.startsWith('mixkit'));
  const n = parseInt(hash(semilla).slice(0, 6), 16);
  const rota = <T,>(xs: T[], k: number) => xs.slice(n % xs.length).concat(xs.slice(0, n % xs.length)).slice(0, k);
  const whoosh = c.filter((e) => e.rol === 'whoosh').sort((a, b) => (a.brilloHz ?? 0) - (b.brilloHz ?? 0));
  const graves = whoosh.slice(0, Math.ceil(whoosh.length / 2));
  const pops = c.filter((e) => e.rol === 'pop' || e.rol === 'click');
  const impactos = c.filter((e) => e.rol === 'impact');
  return {
    whooshes: await Promise.all(rota(graves, 4).map(ref)),
    pops: await Promise.all(rota(pops, 3).map(ref)),
    impacto: impactos.length ? await ref(rota(impactos, 1)[0]) : undefined,
  };
};

/** Un efecto puntual por id del catálogo (p. ej. "mixkit-1234"). */
export const efecto = async (id: string) => {
  const e = catalogo().find((x) => x.id === id);
  if (!e) throw new Error(`No hay efecto ${id} en el catálogo`);
  return ref(e);
};

// --- Íconos ------------------------------------------------------------------

/** "ph:fingerprint-bold" → public/assets/icons/ph__fingerprint-bold.svg */
export const icono = async (id: string) => {
  const [prefijo, nombre] = id.split(':');
  if (!prefijo || !nombre) throw new Error(`Ícono "${id}": usa prefijo:nombre de Iconify`);
  const archivo = `assets/icons/${prefijo}__${nombre}.svg`;
  await bajar(`https://api.iconify.design/${prefijo}/${nombre}.svg`, path.join('public', archivo));
  return archivo;
};

export const segundos = duracion;
