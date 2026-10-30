import React from 'react';
import {Easing, Img, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, pop, recurso, suave} from '../lib/anim';
import {TEXTO, type Tema} from '../lib/temas';
import type {Foco, Visual} from '../lib/types';

/** Zona central del Short: entre el titular y el subtítulo. */
export const ESCENARIO = {top: 420, alto: 900};

const sombra = '0 30px 70px rgba(0,0,0,0.55), 0 8px 18px rgba(0,0,0,0.35)';

/**
 * Cámara hacia un foco: arranca mostrando todo y se acerca con ease-in-out
 * hasta el detalle. Nada lineal.
 */
const camara = (frame: number, total: number, foco?: Foco) => {
  if (!foco) {
    const s = interpolate(frame, [0, total], [1, 1.06], {...clamp, easing: Easing.inOut(Easing.quad)});
    return `scale(${s})`;
  }
  const k = interpolate(frame, [8, Math.max(total - 6, 20)], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const z = 1 + (foco.zoom - 1) * k;
  // Llevar el foco al centro sin destapar el borde: con zoom z solo se puede
  // correr la imagen (1 - 1/z)/2 de su tamaño. Sin este tope, un foco cerca del
  // borde dejaba un pedazo de fondo dentro del marco.
  const tope = 50 * (1 - 1 / z);
  const lim = (v: number) => Math.max(-tope, Math.min(tope, v));
  const dx = lim((0.5 - foco.x) * 100);
  const dy = lim((0.5 - foco.y) * 100);
  return `scale(${z}) translate(${dx}%, ${dy}%)`;
};

const Pagina: React.FC<{src: string; alto: number; rot: number; estilo?: React.CSSProperties}> = ({src, alto, rot, estilo}) => (
  <Img
    src={recurso(src)}
    style={{
      height: alto,
      width: 'auto',
      borderRadius: 6,
      boxShadow: sombra,
      transform: `rotate(${rot}deg)`,
      background: '#fff',
      ...estilo,
    }}
  />
);

export const VisualEscena: React.FC<{visual: Visual; tema: Tema; total: number}> = ({visual, tema, total}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = pop(frame, fps, 0, 13);
  const m = suave(frame, fps);
  const centro: React.CSSProperties = {
    position: 'absolute',
    top: ESCENARIO.top,
    height: ESCENARIO.alto,
    left: 0,
    right: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  };

  if (visual.tipo === 'portada' || visual.tipo === 'imagen') {
    // Entra inclinada en 3D y se endereza; después la cámara busca el foco.
    const foco = visual.tipo === 'imagen' ? visual.foco : undefined;
    return (
      <div style={{...centro, perspective: 1600}}>
        <div
          style={{
            width: 1000,
            borderRadius: 18,
            overflow: 'hidden',
            boxShadow: sombra,
            transform: `rotateX(${interpolate(m, [0, 1], [28, 0])}deg) translateY(${interpolate(m, [0, 1], [260, 0])}px) scale(${interpolate(e, [0, 1], [0.75, 1])})`,
            opacity: interpolate(m, [0, 0.25], [0, 1], clamp),
          }}
        >
          <div style={{transform: camara(frame, total, foco), transformOrigin: 'center'}}>
            <Img src={recurso(visual.src)} style={{width: '100%', display: 'block'}} />
          </div>
        </div>
      </div>
    );
  }

  if (visual.tipo === 'pagina') {
    // Una hoja que se desliza desde la derecha, como si alguien la dejara en la mesa.
    const x = interpolate(m, [0, 1], [900, 0]);
    const rot = interpolate(m, [0, 1], [14, -2]);
    return (
      <div style={centro}>
        <div style={{height: ESCENARIO.alto, overflow: 'visible', transform: `translateX(${x}px) rotate(${rot}deg)`}}>
          <div style={{height: '100%', overflow: 'hidden', borderRadius: 6, boxShadow: sombra}}>
            <div style={{height: '100%', transform: camara(frame, total, visual.foco), transformOrigin: 'center'}}>
              <Pagina src={visual.src} alto={ESCENARIO.alto} rot={0} estilo={{boxShadow: 'none', borderRadius: 0}} />
            </div>
          </div>
          {visual.etiqueta ? (
            <div
              style={{
                position: 'absolute',
                top: -26,
                left: -34,
                padding: '10px 22px',
                background: tema.papel,
                color: '#1d1a16',
                fontFamily: tema.etiqueta,
                fontSize: 40,
                boxShadow: '0 8px 20px rgba(0,0,0,0.4)',
                transform: `rotate(${-6 + 3 * (1 - pop(frame, fps, 8))}deg) scale(${pop(frame, fps, 8)})`,
              }}
            >
              {visual.etiqueta}
            </div>
          ) : null}
        </div>
      </div>
    );
  }

  if (visual.tipo === 'abanico') {
    // Las hojas salen de un mazo y se abren en abanico, una por una.
    const n = visual.srcs.length;
    return (
      <div style={centro}>
        {visual.srcs.map((s, i) => {
          const k = pop(frame, fps, 3 + i * 4, 14);
          const ang = n === 1 ? 0 : -22 + (44 * i) / (n - 1);
          const dx = n === 1 ? 0 : -300 + (600 * i) / (n - 1);
          return (
            <div
              key={s}
              style={{
                position: 'absolute',
                transformOrigin: '50% 120%',
                transform: `translateX(${dx * k}px) translateY(${(1 - k) * 500 + Math.abs(ang) * 3 * k}px) rotate(${ang * k}deg)`,
              }}
            >
              <Pagina src={s} alto={ESCENARIO.alto * 0.78} rot={0} />
            </div>
          );
        })}
      </div>
    );
  }

  if (visual.tipo === 'numero') {
    return (
      <div style={{...centro, flexDirection: 'column'}}>
        <div
          style={{
            fontFamily: tema.display,
            fontWeight: 900,
            fontSize: 420,
            lineHeight: 1,
            color: tema.acento,
            transform: `scale(${interpolate(e, [0, 1], [0.3, 1])}) rotate(${interpolate(e, [0, 1], [-12, -3])}deg)`,
            textShadow: '0 20px 60px rgba(0,0,0,0.45)',
          }}
        >
          {visual.valor}
        </div>
        {visual.sub ? (
          <div
            style={{
              marginTop: 10,
              fontFamily: TEXTO,
              fontWeight: 800,
              fontSize: 64,
              color: tema.tinta,
              textTransform: 'uppercase',
              opacity: interpolate(pop(frame, fps, 8), [0, 1], [0, 1], clamp),
              transform: `translateY(${interpolate(pop(frame, fps, 8), [0, 1], [40, 0])}px)`,
            }}
          >
            {visual.sub}
          </div>
        ) : null}
      </div>
    );
  }

  // cierre: la portada, el nombre y dónde se compra.
  const k2 = pop(frame, fps, 10);
  const k3 = pop(frame, fps, 18);
  return (
    <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: 300}}>
      <div
        style={{
          width: 860,
          borderRadius: 16,
          overflow: 'hidden',
          boxShadow: sombra,
          transform: `scale(${interpolate(e, [0, 1], [0.6, 1])}) rotate(${interpolate(e, [0, 1], [6, -1.5])}deg)`,
        }}
      >
        <Img src={recurso(visual.src)} style={{width: '100%', display: 'block'}} />
      </div>
      <div
        style={{
          marginTop: 60,
          fontFamily: tema.display,
          fontWeight: 900,
          fontSize: 92,
          color: tema.tinta,
          textTransform: tema.mayus ? 'uppercase' : 'none',
          textAlign: 'center',
          padding: '0 60px',
          lineHeight: 1.05,
          transform: `translateY(${interpolate(k2, [0, 1], [60, 0])}px)`,
          opacity: interpolate(k2, [0, 0.4], [0, 1], clamp),
        }}
      >
        {visual.titulo}
      </div>
      {visual.sub ? (
        <div style={{marginTop: 14, fontFamily: TEXTO, fontWeight: 500, fontSize: 46, color: tema.tinta, opacity: 0.85 * interpolate(k2, [0, 0.4], [0, 1], clamp)}}>
          {visual.sub}
        </div>
      ) : null}
      <div
        style={{
          marginTop: 40,
          padding: '18px 40px',
          borderRadius: 999,
          background: tema.acento,
          color: tema.sobreAcento,
          fontFamily: TEXTO,
          fontWeight: 900,
          fontSize: 50,
          transform: `scale(${interpolate(k3, [0, 1], [0.4, 1])})`,
          opacity: interpolate(k3, [0, 0.3], [0, 1], clamp),
        }}
      >
        {visual.linea}
      </div>
    </div>
  );
};
