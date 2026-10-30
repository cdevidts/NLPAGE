/**
 * Arma y renderiza un Short a partir de su plan.
 *
 *   npm run short -- --plan plans/56-cold-case-01-en.json [--solo-check] [--sin-render]
 *
 * 1. Compuerta: el plan se revisa antes de gastar un segundo de render.
 * 2. Voz por escena (Kokoro EN / Piper ES), tiempos de cada palabra con
 *    faster-whisper, y la compuerta de nuevo: si whisper no oye el guion, la
 *    voz salió mal y no se sigue.
 * 3. Música, efectos e íconos (bajados, no dibujados).
 * 4. Render con Remotion, loudness a -14 LUFS / -1 dBTP (estándar de Shorts),
 *    ficha de YouTube y revisión (`npm run watch`).
 */
import fs from 'node:fs';
import path from 'node:path';
import {arg, leerPlan, resolverVisual, ruta, sh, type Plan} from './lib/comun';
import {efecto, efectosBase, icono, musica, palabras, voz} from './lib/medios';
import {revisar} from './watch';
import type {Escena, ShortProps, SfxRef} from '../src/lib/types';

const FPS = 30;
const VOZ_DESDE = 0.15;
const COLA = 0.3;

const planArchivo = arg('plan');
if (!planArchivo) throw new Error('Uso: npm run short -- --plan plans/<slug>.json');
const plan = leerPlan(planArchivo);

// --- 1. Compuerta ------------------------------------------------------------

const compuerta = (p: Plan) => {
  const errores: string[] = [];
  const avisos: string[] = [];
  const existe = (s: string) => fs.existsSync(path.join('public', ruta(p, s)));
  p.escenas.forEach((e, i) => {
    const n = `escena ${i + 1}`;
    if (!e.dice?.trim()) errores.push(`${n}: sin "dice" (cada escena tiene voz)`);
    const srcs = e.visual.tipo === 'abanico' ? e.visual.srcs : 'src' in e.visual ? [e.visual.src] : [];
    for (const s of srcs) if (!existe(s)) errores.push(`${n}: no existe ${ruta(p, s)} (¿corriste npm run producto -- ${p.producto}?)`);
    if (e.texto && e.texto.split(/\s+/).length > 6) avisos.push(`${n}: titular de ${e.texto.split(/\s+/).length} palabras; más de 5 no se alcanza a leer`);
    if (e.dice && e.dice.split(/\s+/).length > 28) avisos.push(`${n}: ${e.dice.split(/\s+/).length} palabras en una escena: córtala en dos`);
  });
  if (!fs.existsSync(path.join('public', ruta(p, p.cierre.src)))) errores.push(`cierre: no existe ${ruta(p, p.cierre.src)}`);
  const palabrasTot = p.escenas.reduce((s, e) => s + e.dice.split(/\s+/).length, 0) + (p.cierre.dice?.split(/\s+/).length ?? 0);
  const estimado = palabrasTot / 2.6 + p.escenas.length * 0.5 + 2.5;
  // Desde oct-2024 un Short puede durar hasta 3 min; sobre 60 s es una prueba (V4 de la bitácora).
  if (estimado > 175) errores.push(`dura ~${estimado.toFixed(0)} s: un Short no puede pasar de 3 min`);
  else if (estimado > 60) avisos.push(`dura ~${estimado.toFixed(0)} s: más de 60 s solo si el plan prueba la duración (V4)`);
  if (estimado < 12) avisos.push(`dura ~${estimado.toFixed(0)} s: muy corto para contar el producto`);
  const primera = p.escenas[0]?.dice.split(/\s+/).length ?? 0;
  if (primera > 12) avisos.push(`el gancho (escena 1) tiene ${primera} palabras: a 2,6 palabras/s no cabe en los primeros 3 s`);
  if (!p.youtube?.titulo || p.youtube.titulo.length > 100) errores.push('youtube.titulo falta o pasa de 100 caracteres');
  if (!p.youtube?.descripcion) errores.push('youtube.descripcion falta');
  return {errores, avisos, estimado};
};

const c = compuerta(plan);
for (const a of c.avisos) console.log(`⚠️  ${a}`);
for (const e of c.errores) console.log(`❌ ${e}`);
if (c.errores.length) process.exit(1);
console.log(`✓ compuerta: ${plan.escenas.length} escenas, ~${c.estimado.toFixed(0)} s estimados`);
if (process.argv.includes('--solo-check')) process.exit(0);

// --- 2. Voz y palabras ---------------------------------------------------------

const dirVoz = path.join('public', 'voz', plan.slug);
fs.mkdirSync(dirVoz, {recursive: true});
const lineas = [...plan.escenas.map((e) => e.dice), plan.cierre.dice ?? ''];
const voces: Array<{src?: string; seg: number; palabras: Escena['palabras']}> = [];
for (const [i, texto] of lineas.entries()) {
  if (!texto) {
    voces.push({seg: 0, palabras: []});
    continue;
  }
  const wav = await voz(texto, plan.idioma, plan.voz, plan.velocidad ?? 1, plan.vozEstilo);
  const destino = path.join(dirVoz, `${String(i + 1).padStart(2, '0')}.wav`);
  fs.copyFileSync(wav, destino);
  const pal = palabras(wav, plan.idioma, texto);
  const seg = Number(sh('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav], {silencio: true}));
  console.log(`  voz ${i + 1}: ${seg.toFixed(2)} s, whisper oye ${pal.coinciden}/${pal.total} palabras, ${(pal.similitud * 100).toFixed(0)} % de las letras`);
  if (pal.similitud < 0.8) {
    console.log(`❌ voz ${i + 1}: whisper oyó "${pal.oido}". La voz pronuncia mal el guion: reescribe la línea (números en letras, siglas separadas).`);
    process.exit(1);
  }
  voces.push({src: path.relative('public', destino), seg, palabras: pal.palabras});
}

// --- 3. Música, efectos, íconos ------------------------------------------------

const base = await efectosBase(plan.slug);
const pm = plan.musica && plan.musica !== 'ninguna' ? plan.musica : null;
const m = pm?.archivo ? {src: pm.archivo, credito: ''} : pm?.incompetech ? await musica(pm.incompetech) : null;

const escenas: Escena[] = [];
for (const [i, e] of plan.escenas.entries()) {
  const v = voces[i];
  escenas.push({
    visual: resolverVisual(plan, e.visual),
    texto: e.texto,
    icono: e.icono ? await icono(e.icono) : undefined,
    voz: v.src,
    vozSeg: v.seg,
    palabras: v.palabras,
    vozDesde: VOZ_DESDE,
    frames: Math.round((VOZ_DESDE + v.seg + COLA + (e.pausa ?? 0)) * FPS),
    sfx: e.sfx ? await efecto(e.sfx) : undefined,
  });
}
const vc = voces[voces.length - 1];
escenas.push({
  visual: {tipo: 'cierre', src: ruta(plan, plan.cierre.src), titulo: plan.cierre.titulo, sub: plan.cierre.sub, linea: plan.cierre.linea},
  voz: vc.src,
  vozSeg: vc.seg,
  palabras: vc.palabras,
  vozDesde: 0.5,
  frames: Math.round(Math.max(3.2, 0.5 + vc.seg + 1.2) * FPS),
});

const props: ShortProps = {
  tema: plan.tema,
  escenas,
  musica: m
    ? {src: m.src, volumen: (plan.musica as {volumen?: number}).volumen ?? 0.25, desdeSeg: (plan.musica as {desde?: number}).desde ?? 0}
    : undefined,
  whooshes: base.whooshes,
  pops: base.pops,
  impacto: base.impacto as SfxRef | undefined,
  sfxVolumen: 0.55,
  marca: 'SheetSmithChile',
};
fs.mkdirSync('out', {recursive: true});
const propsArchivo = path.join('out', `${plan.slug}.props.json`);
fs.writeFileSync(propsArchivo, JSON.stringify(props, null, 1));
const total = escenas.reduce((s, e) => s + e.frames, 0) / FPS;
console.log(`✓ props: ${escenas.length} escenas, ${total.toFixed(1)} s → ${propsArchivo}`);

// Ficha de YouTube junto al video: título, descripción con crédito de música, tags.
fs.mkdirSync('renders', {recursive: true});
const ficha = [
  `# ${plan.youtube.titulo}`,
  '',
  plan.youtube.descripcion.trim(),
  '',
  m ? m.credito : '',
  '',
  `Tags: ${plan.youtube.tags.join(', ')}`,
  '',
].join('\n');
fs.writeFileSync(path.join('renders', `${plan.slug}.youtube.md`), ficha);
if (process.argv.includes('--sin-render')) process.exit(0);

// --- 4. Render y loudness --------------------------------------------------------

const crudo = path.join('out', `${plan.slug}.raw.mp4`);
sh('npx', ['remotion', 'render', 'src/index.ts', 'Short', crudo, `--props=${propsArchivo}`, '--concurrency=4', '--log=error']);
const final = path.join('renders', `${plan.slug}.mp4`);
// Loudnorm en dos pasadas: la primera mide y la segunda corrige lineal. En una
// sola pasada el pico quedó en -0,5 dBTP (sobre el -1 que piden las plataformas).
const medida = sh('bash', ['-c', `ffmpeg -nostats -i "${crudo}" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | tail -12`], {silencio: true});
const ln = JSON.parse(medida.slice(medida.indexOf('{'))) as Record<string, string>;
const filtro = `loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=${ln.input_i}:measured_TP=${ln.input_tp}:measured_LRA=${ln.input_lra}:measured_thresh=${ln.input_thresh}:offset=${ln.target_offset}:linear=true`;
sh('ffmpeg', ['-y', '-v', 'error', '-i', crudo, '-c:v', 'copy', '-af', filtro, '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', final]);
console.log(`✓ render: ${final}`);
await revisar(final, plan.idioma);
