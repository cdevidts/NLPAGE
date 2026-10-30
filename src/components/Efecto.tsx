import React from 'react';
import {Audio, Sequence, useVideoConfig} from 'remotion';
import {recurso} from '../lib/anim';
import type {SfxRef} from '../lib/types';

/**
 * Un efecto cuyo PICO cae en el frame `en` (técnica de Videos-Next-Layer: lo
 * que se alinea con el corte es el golpe, no el inicio del archivo). Si el pico
 * está más adentro que el espacio disponible, se recorta el inicio.
 */
export const EfectoEn: React.FC<{efecto: SfxRef; en: number; volumen: number}> = ({efecto, en, volumen}) => {
  const {fps} = useVideoConfig();
  const pico = Math.round(efecto.picoSeg * fps);
  const desde = en - pico;
  const recorte = Math.max(0, -desde);
  const g = volumen * 10 ** (efecto.gananciaDb / 20);
  return (
    <Sequence from={Math.max(desde, 0)} durationInFrames={pico - recorte + Math.round(fps * 2.5)} name={`SFX ${efecto.id ?? ''}`}>
      <Audio src={recurso(efecto.src)} trimBefore={recorte || undefined} volume={g} />
    </Sequence>
  );
};
