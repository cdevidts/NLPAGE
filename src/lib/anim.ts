import {interpolate, spring, staticFile} from 'remotion';

export const recurso = (s: string) =>
  /^(https?:|data:)/.test(s) ? s : staticFile(s.replace(/^\/?public\//, '').replace(/^\//, ''));

/** Rebote con sobrepaso: el elemento "llega", no "aparece". */
export const pop = (frame: number, fps: number, delay = 0, damping = 11) =>
  spring({frame: frame - delay, fps, config: {damping, stiffness: 160, mass: 0.55}, durationInFrames: 24});

/** Resorte sin sobrepaso para movimientos grandes (páginas, cámara). */
export const suave = (frame: number, fps: number, delay = 0) =>
  spring({frame: frame - delay, fps, config: {damping: 200}, durationInFrames: 26});

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const entre = (f: number, a: number, b: number, de: number, a2: number) =>
  interpolate(f, [a, b], [de, a2], clamp);

/** Contorno por capas de sombra: legible sobre cualquier fondo sin caja. */
export const contorno = (size = 5, color = '#07080C') =>
  [
    `${size}px ${size}px 0 ${color}`,
    `-${size}px -${size}px 0 ${color}`,
    `${size}px -${size}px 0 ${color}`,
    `-${size}px ${size}px 0 ${color}`,
    `0 ${size}px 0 ${color}`,
    `0 -${size}px 0 ${color}`,
    `${size}px 0 0 ${color}`,
    `-${size}px 0 0 ${color}`,
    `0 ${Math.round(size * 1.6)}px 24px rgba(0,0,0,0.7)`,
  ].join(', ');

/** Separa "Un *caso* sin resolver" en palabras con su marca de resaltado. */
export const partir = (texto: string) =>
  texto
    .split(/\s+/)
    .filter(Boolean)
    .map((w) => ({w: w.replace(/\*/g, ''), marcada: /\*/.test(w)}));
