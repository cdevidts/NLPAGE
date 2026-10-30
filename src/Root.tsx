import React from 'react';
import {Composition} from 'remotion';
import {EtsyLoop} from './EtsyLoop';
import {Short} from './Short';
import type {LoopProps, ShortProps} from './lib/types';

const FPS = 30;

const shortVacio: ShortProps = {
  tema: 'coldcase',
  escenas: [
    {visual: {tipo: 'numero', valor: '39', sub: 'evidence files'}, texto: 'Can you *solve* it?', palabras: [], vozDesde: 0.12, frames: 90},
  ],
  whooshes: [],
  pops: [],
  sfxVolumen: 0.6,
  marca: 'SheetSmithChile',
};

const loopVacio: LoopProps = {tema: 'coldcase', paginas: [], titulo: 'Title', sub: 'Sub', frases: ['One'], marca: 'SheetSmithChile'};

/** Los props reales los arma `npm run short` / `npm run loop` y los pasa con --props. */
export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="Short"
      component={Short}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={90}
      defaultProps={shortVacio}
      calculateMetadata={({props}) => ({durationInFrames: Math.max(1, props.escenas.reduce((s, e) => s + e.frames, 0))})}
    />
    <Composition id="EtsyLoop" component={EtsyLoop} width={1920} height={1440} fps={FPS} durationInFrames={FPS * 10} defaultProps={loopVacio} />
  </>
);
