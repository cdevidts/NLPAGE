import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, contorno, partir, pop} from '../lib/anim';
import {TEXTO, type Tema} from '../lib/temas';
import type {Palabra} from '../lib/types';

/**
 * Titular cinético: cada palabra llega con rebote, una tras otra; la marcada
 * con *asteriscos* lleva una caja del color de acento detrás. Va arriba, lejos
 * de los subtítulos y de la interfaz de YouTube (abajo y a la derecha).
 */
export const Titular: React.FC<{texto: string; tema: Tema; top?: number; size?: number}> = ({
  texto,
  tema,
  top = 200,
  size = 104,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const palabras = partir(texto);
  return (
    <div
      style={{
        position: 'absolute',
        top,
        left: 70,
        right: 70,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: `${size * 0.12}px ${size * 0.24}px`,
        fontFamily: tema.display,
        fontWeight: 900,
        fontSize: size,
        lineHeight: 1.04,
        textTransform: tema.mayus ? 'uppercase' : 'none',
        letterSpacing: tema.mayus ? 1 : -1,
      }}
    >
      {palabras.map((p, i) => {
        const e = pop(frame, fps, 2 + i * 3);
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              transform: `translateY(${interpolate(e, [0, 1], [50, 0])}px) scale(${interpolate(e, [0, 1], [0.6, 1])})`,
              opacity: interpolate(e, [0, 0.3], [0, 1], clamp),
              color: p.marcada ? tema.sobreAcento : tema.tinta,
              background: p.marcada ? tema.acento : 'transparent',
              padding: p.marcada ? `0 ${size * 0.14}px` : 0,
              borderRadius: p.marcada ? 10 : 0,
              textShadow: p.marcada ? 'none' : `0 6px 28px rgba(0,0,0,${tema.tinta === '#13261b' ? 0.08 : 0.55})`,
            }}
          >
            {p.w}
          </span>
        );
      })}
    </div>
  );
};

/** Hasta 3 palabras por pantalla; corta antes si hay pausa o puntuación. */
export const agrupar = (palabras: Palabra[]) => {
  const grupos: Palabra[][] = [];
  let actual: Palabra[] = [];
  for (const p of palabras) {
    const previa = actual[actual.length - 1];
    if (actual.length >= 3 || (previa && (p.s - previa.e > 0.35 || /[.,!?;:]$/.test(previa.w)))) {
      grupos.push(actual);
      actual = [];
    }
    actual.push(p);
  }
  if (actual.length) grupos.push(actual);
  return grupos;
};

/**
 * Subtítulo karaoke: dice exactamente lo que suena. La palabra que se escucha
 * se marca con un resaltador que la barre mientras dura.
 */
export const Subtitulo: React.FC<{palabras: Palabra[]; desde: number; tema: Tema; top?: number}> = ({
  palabras,
  desde,
  tema,
  top = 1385,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps - desde;
  const grupos = React.useMemo(() => agrupar(palabras), [palabras]);
  const idx = grupos.findIndex((g, i) => t >= g[0].s - 0.08 && (i === grupos.length - 1 ? t < g[g.length - 1].e + 0.4 : t < grupos[i + 1][0].s - 0.08));
  if (idx === -1) return null;
  const g = grupos[idx];
  const inicio = Math.round((g[0].s - 0.08 + desde) * fps);
  return (
    <div
      style={{
        position: 'absolute',
        top,
        left: 60,
        right: 60,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: '6px 18px',
        fontFamily: TEXTO,
        fontWeight: 900,
        fontSize: 82,
        lineHeight: 1.1,
        color: '#ffffff',
        textTransform: 'uppercase',
      }}
    >
      {g.map((p, i) => {
        const e = pop(frame, fps, inicio + i * 2);
        const barrido = interpolate(t, [p.s, Math.max(p.e, p.s + 0.12)], [0, 100], clamp);
        // Solo la palabra que suena ahora lleva el resaltador.
        const siguiente = g[i + 1]?.s ?? p.e + 0.4;
        const suena = t >= p.s - 0.03 && t < siguiente - 0.03;
        return (
          <span key={i} style={{position: 'relative', display: 'inline-block', transform: `scale(${interpolate(e, [0, 1], [0.7, 1])})`}}>
            {suena ? (
              <span
                style={{
                  position: 'absolute',
                  left: -10,
                  top: 6,
                  bottom: 2,
                  width: `calc(${barrido}% + 20px)`,
                  background: tema.acento,
                  borderRadius: 10,
                  transform: 'rotate(-1.5deg)',
                }}
              />
            ) : null}
            <span style={{position: 'relative', textShadow: contorno(5)}}>{p.w.replace(/[.,!?;:]+$/, '')}</span>
          </span>
        );
      })}
    </div>
  );
};
