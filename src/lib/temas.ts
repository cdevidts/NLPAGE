import type {TemaId} from './types';

/**
 * Cada línea de producto tiene su propio mundo visual, el mismo de sus fotos de
 * Etsy: así el Short, la portada y el listing se reconocen como una sola cosa.
 * SheetSmithChile es la tienda, no una estética: lo que une a los cuatro temas
 * es el movimiento (resorte, sobrepaso, cortes secos) y la marca chica arriba.
 */
export type Tema = {
  fondo: string;
  /** Color de los titulares sobre el fondo. */
  tinta: string;
  /** El color que se mueve: resaltador, sellos, barra del cierre. */
  acento: string;
  /** Texto sobre el acento. */
  sobreAcento: string;
  papel: string;
  display: string;
  /** Mayúsculas en el titular. */
  mayus: boolean;
  /** Tipografía de etiquetas chicas (evidencia, notas). */
  etiqueta: string;
  /** Viñeta y grano: más en los temas oscuros. */
  vineta: number;
  grano: number;
};

const INTER = 'Inter, "Helvetica Neue", Arial, sans-serif';

const NAVIDAD: Tema = {
  fondo: 'radial-gradient(120% 90% at 50% 30%, #9b2226 0%, #6e1519 60%, #3d0b0e 100%)',
  tinta: '#fbf6ec',
  acento: '#e2b84a',
  sobreAcento: '#3d0b0e',
  papel: '#fffdf8',
  display: '"Playfair Display", Georgia, serif',
  mayus: false,
  etiqueta: INTER,
  vineta: 0.35,
  grano: 0.04,
};

export const TEMAS: Record<TemaId, Tema> = {
  coldcase: {
    fondo: 'radial-gradient(120% 90% at 50% 35%, #3a2a1d 0%, #1c140e 55%, #0b0806 100%)',
    tinta: '#f3ead6',
    acento: '#c8352b',
    sobreAcento: '#fff6ea',
    papel: '#efe6d2',
    display: 'Oswald, "Arial Narrow", Impact, sans-serif',
    mayus: true,
    etiqueta: '"Special Elite", "Courier New", monospace',
    vineta: 0.55,
    grano: 0.07,
  },
  piano: NAVIDAD,
  // Juegos de Navidad (escape room): el mismo mundo rojo y dorado del piano navideño.
  navidad: NAVIDAD,
  clasicos: {
    fondo: 'radial-gradient(120% 90% at 50% 30%, #2b4a78 0%, #1b3156 60%, #0d1a30 100%)',
    tinta: '#fbf6ec',
    acento: '#e2b84a',
    sobreAcento: '#0d1a30',
    papel: '#fffdf8',
    display: '"Playfair Display", Georgia, serif',
    mayus: false,
    etiqueta: INTER,
    vineta: 0.35,
    grano: 0.04,
  },
  sheets: {
    fondo: 'radial-gradient(120% 90% at 50% 30%, #ffffff 0%, #eef5f0 60%, #d9e9de 100%)',
    tinta: '#13261b',
    acento: '#188038',
    sobreAcento: '#ffffff',
    papel: '#ffffff',
    display: INTER,
    mayus: false,
    etiqueta: INTER,
    vineta: 0.12,
    grano: 0.025,
  },
  fiesta: {
    fondo: 'radial-gradient(120% 90% at 50% 30%, #23366b 0%, #14213d 60%, #0a1122 100%)',
    tinta: '#ffffff',
    acento: '#fca311',
    sobreAcento: '#14213d',
    papel: '#ffffff',
    display: INTER,
    mayus: true,
    etiqueta: INTER,
    vineta: 0.4,
    grano: 0.05,
  },
};

export const TEXTO = INTER;
