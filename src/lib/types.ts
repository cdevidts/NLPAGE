/** Lo que comparten los scripts (que arman los props) y las composiciones. */

export type TemaId = 'coldcase' | 'piano' | 'sheets' | 'fiesta';

/** Un efecto medido del catálogo: su pico es lo que se alinea con el evento. */
export type SfxRef = {id?: string; src: string; picoSeg: number; gananciaDb: number};

/** Una palabra dicha, con tiempos en segundos desde el inicio de la escena. */
export type Palabra = {w: string; s: number; e: number};

/** Zona de una página o imagen a la que se acerca la cámara (0-1 del ancho/alto). */
export type Foco = {x: number; y: number; zoom: number};

export type Visual =
  | {tipo: 'portada'; src: string}
  | {tipo: 'pagina'; src: string; foco?: Foco; etiqueta?: string}
  | {tipo: 'abanico'; srcs: string[]}
  | {tipo: 'imagen'; src: string; foco?: Foco}
  | {tipo: 'numero'; valor: string; sub?: string}
  | {tipo: 'cierre'; src: string; titulo: string; sub?: string; linea: string};

export type Escena = {
  visual: Visual;
  /** Titular cinético arriba. `*palabra*` va resaltada. Corto: 2-5 palabras. */
  texto?: string;
  /** Ícono de Iconify ya bajado (ruta en public/). */
  icono?: string;
  /** Voz en off de la escena (ruta en public/) y sus palabras con tiempo. */
  voz?: string;
  vozSeg?: number;
  palabras: Palabra[];
  /** Cuándo empieza a sonar la voz dentro de la escena (s). */
  vozDesde: number;
  frames: number;
  sfx?: SfxRef;
};

export type ShortProps = {
  tema: TemaId;
  escenas: Escena[];
  musica?: {src: string; volumen: number; desdeSeg?: number};
  whooshes: SfxRef[];
  pops: SfxRef[];
  impacto?: SfxRef;
  sfxVolumen: number;
  /** Texto chico fijo arriba (nombre de la tienda). */
  marca: string;
};

export type LoopProps = {
  tema: TemaId;
  paginas: string[];
  titulo: string;
  sub: string;
  frases: string[];
  marca: string;
};
