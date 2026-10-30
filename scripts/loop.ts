/**
 * Video del listing de Etsy y GIF, desde la sección "loop" del plan.
 *
 *   npm run loop -- --plan plans/56-cold-case-01-en.json
 *
 * renders/<producto>-etsy.mp4  1920x1440 (4:3 como las fotos), 10 s, sin audio
 *                              (Etsy lo muestra mudo y en bucle; pide 5-15 s).
 * renders/<producto>-etsy.gif  800x600 a 10 fps, para donde no se puede subir video.
 */
import fs from 'node:fs';
import path from 'node:path';
import {arg, leerPlan, ruta, sh} from './lib/comun';
import {revisar} from './watch';
import type {LoopProps} from '../src/lib/types';

const plan = leerPlan(arg('plan') ?? '');
if (!plan.loop) throw new Error('El plan no tiene sección "loop"');
const faltan = plan.loop.paginas.map((s) => ruta(plan, s)).filter((s) => !fs.existsSync(path.join('public', s)));
if (faltan.length) throw new Error(`No existen: ${faltan.join(', ')} (npm run producto -- ${plan.producto})`);

const props: LoopProps = {
  tema: plan.tema,
  paginas: plan.loop.paginas.map((s) => ruta(plan, s)),
  titulo: plan.loop.titulo,
  sub: plan.loop.sub,
  frases: plan.loop.frases,
  marca: 'SheetSmithChile',
};
fs.mkdirSync('out', {recursive: true});
const propsArchivo = path.join('out', `${plan.producto}-etsy.props.json`);
fs.writeFileSync(propsArchivo, JSON.stringify(props, null, 1));
const crudo = path.join('out', `${plan.producto}-etsy.raw.mp4`);
sh('npx', ['remotion', 'render', 'src/index.ts', 'EtsyLoop', crudo, `--props=${propsArchivo}`, '--concurrency=4', '--muted', '--log=error']);
fs.mkdirSync('renders', {recursive: true});
const mp4 = path.join('renders', `${plan.producto}-etsy.mp4`);
sh('ffmpeg', ['-y', '-v', 'error', '-i', crudo, '-an', '-c:v', 'libx264', '-crf', '22', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', mp4]);
const gif = path.join('renders', `${plan.producto}-etsy.gif`);
sh('ffmpeg', ['-y', '-v', 'error', '-i', crudo, '-vf', 'fps=10,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=sierra2_4a', '-loop', '0', gif]);
console.log(`✓ ${mp4} (${(fs.statSync(mp4).size / 1e6).toFixed(1)} MB)  ${gif} (${(fs.statSync(gif).size / 1e6).toFixed(1)} MB)`);
await revisar(mp4, plan.idioma);
