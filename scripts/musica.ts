/**
 * Busca música de cama en el catálogo de Kevin MacLeod (incompetech, CC BY 4.0).
 *
 *   npm run musica -- --buscar "mysterious suspense"     # por ánimo, género o instrumento
 *
 * Se elige por el ánimo del video, no por el nombre. Va al plan como
 * "musica": {"incompetech": "<título exacto>", "volumen": 0.25, "desde": 0}.
 */
import {arg} from './lib/comun';
import {catalogoMusica} from './lib/medios';

const q = (arg('buscar') ?? '').toLowerCase().split(/\s+/).filter(Boolean);
const piezas = await catalogoMusica();
const puntaje = (p: (typeof piezas)[number]) => {
  const txt = `${p.title} ${p.feel} ${p.description} ${p.instruments}`.toLowerCase();
  return q.reduce((s, w) => s + (txt.includes(w) ? 1 : 0), 0);
};
const top = piezas
  .map((p) => ({p, s: puntaje(p)}))
  .filter((x) => x.s > 0)
  .sort((a, b) => b.s - a.s)
  .slice(0, 25);
for (const {p, s} of top) console.log(`${s}  ${p.title.padEnd(34)} ${p.length}  ${String(p.bpm).padStart(4)} bpm  ${p.feel} — ${p.description.slice(0, 80)}`);
if (!top.length) console.log('Nada. Prueba con ánimos en inglés: mysterious, dark, bright, calm, playful, christmas, piano.');
