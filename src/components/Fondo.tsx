import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import type {Tema} from '../lib/temas';

const GRANO =
  'data:image/svg+xml;utf8,' +
  encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="220" height="220"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="220" height="220" filter="url(#n)" opacity="0.6"/></svg>',
  );

/** Fondo del tema, viñeta y grano animado. El grano evita el "plano digital". */
export const Fondo: React.FC<{tema: Tema; children?: React.ReactNode}> = ({tema, children}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: tema.fondo}}>
      {children}
      <AbsoluteFill
        style={{background: `radial-gradient(90% 70% at 50% 45%, rgba(0,0,0,0) 50%, rgba(0,0,0,${tema.vineta}) 100%)`}}
      />
      <AbsoluteFill
        style={{
          backgroundImage: `url("${GRANO}")`,
          backgroundSize: '220px 220px',
          backgroundPosition: `${(frame * 53) % 220}px ${(frame * 89) % 220}px`,
          opacity: tema.grano,
          mixBlendMode: 'overlay',
        }}
      />
    </AbsoluteFill>
  );
};
