import {cancelRender, continueRender, delayRender, staticFile} from 'remotion';
import {FONT_FACES} from '../fonts.generated';

/**
 * Tipografías desde public/fonts/ (las baja `npm run setup`), declaradas con
 * reglas `@font-face` en una hoja de estilo. Copiado de Videos-Next-Layer, donde
 * se pagó la lección: con `new FontFace()` + `document.fonts.add()` el
 * `remotion render` pinta parte del texto con la fuente de respaldo aunque
 * `document.fonts.check()` diga que cargó.
 */
const handle = delayRender('Cargando tipografías');

const CSS = FONT_FACES.map(
  (f) =>
    `@font-face{font-family:"${f.family}";src:url("${staticFile(f.file)}") format("woff2");font-weight:${f.weight};font-style:normal;font-display:block;unicode-range:${f.range};}`,
).join('\n');

const cargar = async () => {
  if (typeof document === 'undefined') return;
  const style = document.createElement('style');
  style.textContent = CSS;
  document.head.appendChild(style);
  // Un @font-face se descarga recién cuando algo lo usa: se piden todas ahora.
  await Promise.all(
    FONT_FACES.map((f) => document.fonts.load(`${f.weight} 100px "${f.family}"`, 'AÁñ').catch(() => undefined)),
  );
  await document.fonts.ready;
};

cargar()
  .then(() => continueRender(handle))
  .catch((e) => cancelRender(e));
