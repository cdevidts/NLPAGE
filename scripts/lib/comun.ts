import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import type {TemaId, Visual} from '../../src/lib/types';

/** Carpeta de productos de la tienda (la carpeta compartida del proyecto). */
export const ETSY_DIR = process.env.ETSY_DIR ?? '/mnt/project-files/etsy';

export const sh = (cmd: string, args: string[], opts: {silencio?: boolean} = {}) => {
  const r = spawnSync(cmd, args, {stdio: opts.silencio ? 'pipe' : ['ignore', 'pipe', 'inherit'], maxBuffer: 512 * 1024 * 1024});
  if (r.status !== 0) throw new Error(`${cmd} ${args.slice(0, 3).join(' ')}… falló (${r.status})\n${r.stderr?.toString().slice(-800) ?? ''}`);
  return r.stdout?.toString() ?? '';
};

export const hash = (s: string) => crypto.createHash('sha1').update(s).digest('hex').slice(0, 12);

export const arg = (nombre: string) => {
  const i = process.argv.indexOf(`--${nombre}`);
  return i >= 0 ? process.argv[i + 1] : undefined;
};

export const duracion = (archivo: string) =>
  Number(sh('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', archivo], {silencio: true}).trim());

export const bajar = async (url: string, destino: string) => {
  if (fs.existsSync(destino) && fs.statSync(destino).size > 200) return destino;
  const r = await fetch(url);
  if (!r.ok) throw new Error(`HTTP ${r.status} ${url}`);
  fs.mkdirSync(path.dirname(destino), {recursive: true});
  fs.writeFileSync(destino, Buffer.from(await r.arrayBuffer()));
  return destino;
};

// --- El plan ---------------------------------------------------------------

/**
 * `visual` acepta atajos para no escribir rutas: "foto:01" es la foto 01.jpg
 * del listing y "pag:en:7" la página 7 del PDF con alias "en" (los alias los
 * imprime `npm run producto`).
 */
export type PlanEscena = {
  dice: string;
  texto?: string;
  visual: Visual;
  icono?: string;
  sfx?: string;
  /** Silencio extra al final de la escena (s), para dejar respirar. */
  pausa?: number;
};

export type Plan = {
  slug: string;
  producto: string;
  idioma: 'en' | 'es';
  tema: TemaId;
  voz?: string;
  velocidad?: number;
  /** `incompetech`: título del catálogo de Kevin MacLeod. `archivo`: audio propio
   * (p. ej. la pista de práctica del producto), ruta en public/. */
  musica?: {incompetech?: string; archivo?: string; volumen?: number; desde?: number} | 'ninguna';
  escenas: PlanEscena[];
  cierre: {dice?: string; titulo: string; sub?: string; linea: string; src: string};
  youtube: {titulo: string; descripcion: string; tags: string[]};
  loop?: {paginas: string[]; titulo: string; sub: string; frases: string[]};
  notas?: string;
};

export const leerPlan = (archivo: string) => JSON.parse(fs.readFileSync(archivo, 'utf8')) as Plan;

/** Resuelve un atajo a una ruta relativa a public/. */
export const ruta = (plan: Plan, s: string) => {
  const foto = /^foto:(\d+)$/.exec(s);
  if (foto) return `productos/${plan.producto}/fotos/${foto[1].padStart(2, '0')}.jpg`;
  const pag = /^pag:([\w-]+):(\d+)$/.exec(s);
  if (pag) return `productos/${plan.producto}/paginas-${pag[1]}/${pag[2].padStart(2, '0')}.jpg`;
  return s.replace(/^\/?public\//, '');
};

export const resolverVisual = (plan: Plan, v: Visual): Visual => {
  if (v.tipo === 'abanico') return {...v, srcs: v.srcs.map((s) => ruta(plan, s))};
  if ('src' in v) return {...v, src: ruta(plan, v.src)} as Visual;
  return v;
};
