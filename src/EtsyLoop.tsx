import React from 'react';
import {Img, interpolate, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import './lib/fonts';
import {Fondo} from './components/Fondo';
import {clamp, pop, recurso} from './lib/anim';
import {TEMAS, TEXTO} from './lib/temas';
import type {LoopProps} from './lib/types';

/**
 * Video del listing de Etsy (4:3, como las fotos; Etsy lo muestra mudo y en
 * bucle). Un mazo de páginas reales del producto que se van pasando, y a la
 * derecha el nombre y tres frases que rotan. El último frame es igual al
 * primero: el bucle no salta.
 */
export const EtsyLoop: React.FC<LoopProps> = ({tema: temaId, paginas, titulo, sub, frases, marca}) => {
  const frame = useCurrentFrame();
  const {durationInFrames, fps} = useVideoConfig();
  const tema = TEMAS[temaId];
  const n = paginas.length;
  const L = durationInFrames / n;
  const actual = Math.floor(frame / L);
  const u = (frame - actual * L) / L;
  // La hoja de arriba se va en el último 30 % de su turno.
  const sale = interpolate(u, [0.7, 1], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const ALTO = 1100;

  const capas = [3, 2, 1, 0].map((prof) => {
    const idx = (actual + prof) % n;
    // Mientras la de arriba sale, las de abajo suben un puesto.
    const p = prof - (prof > 0 ? sale : 0);
    const base = {rot: interpolate(p, [0, 1, 2, 3], [-2, 3.5, -4.5, 5]), dx: p * 26, dy: p * 18, esc: 1 - p * 0.035};
    const fuera = prof === 0 ? sale : 0;
    return (
      <div
        key={`${idx}-${prof}`}
        style={{
          position: 'absolute',
          left: 90 + base.dx + fuera * 1100,
          top: 150 + base.dy - fuera * 60,
          transform: `rotate(${base.rot + fuera * 24}deg) scale(${base.esc})`,
          transformOrigin: '50% 60%',
          opacity: prof === 3 ? interpolate(sale, [0, 1], [0, 1]) : 1,
        }}
      >
        <Img
          src={recurso(paginas[idx])}
          style={{height: ALTO, borderRadius: 6, background: '#fff', boxShadow: '0 30px 70px rgba(0,0,0,0.55), 0 8px 18px rgba(0,0,0,0.35)'}}
        />
      </div>
    );
  });

  const M = durationInFrames / frases.length;
  const fi = Math.floor(frame / M);
  const fl = frame - fi * M;
  const ent = pop(fl, fps, 4);
  const sal = interpolate(fl, [M - 10, M - 2], [1, 0], clamp);

  return (
    <Fondo tema={tema}>
      {capas}
      <div style={{position: 'absolute', left: 1080, right: 90, top: 250, display: 'flex', flexDirection: 'column', gap: 30}}>
        <div
          style={{
            fontFamily: tema.display,
            fontWeight: 900,
            fontSize: 120,
            lineHeight: 1.02,
            color: tema.tinta,
            textTransform: tema.mayus ? 'uppercase' : 'none',
          }}
        >
          {titulo}
        </div>
        <div style={{fontFamily: TEXTO, fontWeight: 500, fontSize: 50, color: tema.tinta, opacity: 0.85}}>{sub}</div>
        <div style={{height: 6, width: 160, background: tema.acento, borderRadius: 3, marginTop: 10}} />
        <div style={{height: 260, position: 'relative', marginTop: 20}}>
          <div
            style={{
              display: 'inline-block',
              padding: '18px 34px',
              borderRadius: 14,
              background: tema.acento,
              color: tema.sobreAcento,
              fontFamily: TEXTO,
              fontWeight: 900,
              fontSize: 62,
              lineHeight: 1.1,
              transform: `scale(${interpolate(ent, [0, 1], [0.5, 1])}) rotate(${interpolate(ent, [0, 1], [-8, -1.5])}deg)`,
              transformOrigin: '0% 50%',
              opacity: Math.min(interpolate(ent, [0, 0.3], [0, 1], clamp), sal),
            }}
          >
            {frases[fi % frases.length]}
          </div>
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          right: 90,
          bottom: 70,
          fontFamily: TEXTO,
          fontWeight: 800,
          fontSize: 36,
          letterSpacing: 6,
          textTransform: 'uppercase',
          color: tema.tinta,
          opacity: 0.6,
        }}
      >
        {marca}
      </div>
    </Fondo>
  );
};
