import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, useCurrentFrame, useVideoConfig} from 'remotion';
import './lib/fonts';
import {EfectoEn} from './components/Efecto';
import {Fondo} from './components/Fondo';
import {Subtitulo, Titular} from './components/Texto';
import {VisualEscena} from './components/Visual';
import {clamp, pop, recurso} from './lib/anim';
import {TEMAS, TEXTO, type Tema} from './lib/temas';
import type {Escena, ShortProps} from './lib/types';

export const inicios = (escenas: Escena[]) => {
  const r: number[] = [];
  let acc = 0;
  for (const e of escenas) {
    r.push(acc);
    acc += e.frames;
  }
  return r;
};

/** Ícono de Iconify teñido con el acento vía máscara, junto al titular. */
const Icono: React.FC<{src: string; tema: Tema}> = ({src, tema}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = pop(frame, fps, 6);
  return (
    <div
      style={{
        position: 'absolute',
        right: 70,
        top: 1180,
        width: 150,
        height: 150,
        backgroundColor: tema.acento,
        maskImage: `url(${recurso(src)})`,
        WebkitMaskImage: `url(${recurso(src)})`,
        maskSize: 'contain',
        WebkitMaskSize: 'contain',
        maskRepeat: 'no-repeat',
        WebkitMaskRepeat: 'no-repeat',
        filter: 'drop-shadow(0 8px 20px rgba(0,0,0,0.6))',
        transform: `scale(${interpolate(e, [0, 1], [0.3, 1])}) rotate(${interpolate(e, [0, 1], [-18, 0])}deg)`,
        opacity: interpolate(e, [0, 0.3], [0, 1], clamp),
      }}
    />
  );
};

const EscenaVista: React.FC<{escena: Escena; tema: Tema}> = ({escena, tema}) => (
  <AbsoluteFill>
    <VisualEscena visual={escena.visual} tema={tema} total={escena.frames} />
    {escena.texto && escena.visual.tipo !== 'cierre' ? <Titular texto={escena.texto} tema={tema} /> : null}
    {escena.icono ? <Icono src={escena.icono} tema={tema} /> : null}
    {escena.visual.tipo !== 'cierre' ? <Subtitulo palabras={escena.palabras} desde={escena.vozDesde} tema={tema} /> : null}
  </AbsoluteFill>
);

/**
 * El Short: escenas en fila con cortes secos, una voz por escena, música de
 * cama que baja sola cuando hay voz, whoosh en cada cambio de escena y golpe en
 * el cierre.
 */
export const Short: React.FC<ShortProps> = (p) => {
  const tema = TEMAS[p.tema];
  const {fps} = useVideoConfig();
  const ini = inicios(p.escenas);

  // Tramos con voz, en frames globales, para el ducking de la música.
  const tramos = p.escenas
    .map((e, i) => (e.voz ? [ini[i] + e.vozDesde * fps, ini[i] + (e.vozDesde + (e.vozSeg ?? 0)) * fps] : null))
    .filter(Boolean) as Array<[number, number]>;
  const conVoz = (f: number) =>
    tramos.reduce((m, [a, b]) => Math.max(m, interpolate(f, [a - 6, a, b, b + 9], [0, 1, 1, 0], clamp)), 0);

  return (
    <Fondo tema={tema}>
      {p.escenas.map((e, i) => (
        <Sequence key={i} from={ini[i]} durationInFrames={e.frames} name={`Escena ${i + 1} ${e.visual.tipo}`}>
          <EscenaVista escena={e} tema={tema} />
          {e.voz ? (
            <Sequence from={Math.round(e.vozDesde * fps)} name="Voz">
              <Audio src={recurso(e.voz)} />
            </Sequence>
          ) : null}
        </Sequence>
      ))}

      <div
        style={{
          position: 'absolute',
          top: 120,
          width: '100%',
          textAlign: 'center',
          fontFamily: TEXTO,
          fontWeight: 800,
          fontSize: 34,
          letterSpacing: 6,
          textTransform: 'uppercase',
          color: tema.tinta,
          opacity: 0.6,
        }}
      >
        {p.marca}
      </div>

      {p.musica ? (
        <Audio
          src={recurso(p.musica.src)}
          trimBefore={Math.round((p.musica.desdeSeg ?? 0) * fps) || undefined}
          volume={(f) => p.musica!.volumen * (1 - 0.7 * conVoz(f)) * interpolate(f, [0, 8], [0, 1], clamp)}
        />
      ) : null}

      {ini.slice(1).map((f, i) =>
        p.whooshes.length ? (
          <EfectoEn key={`w${i}`} efecto={p.whooshes[i % p.whooshes.length]} en={f} volumen={p.sfxVolumen * 0.8} />
        ) : null,
      )}
      {p.escenas.map((e, i) =>
        e.sfx ? <EfectoEn key={`s${i}`} efecto={e.sfx} en={ini[i] + 4} volumen={p.sfxVolumen} /> : null,
      )}
      {p.escenas.map((e, i) =>
        e.icono && p.pops.length ? (
          <EfectoEn key={`p${i}`} efecto={p.pops[i % p.pops.length]} en={ini[i] + 8} volumen={p.sfxVolumen * 0.7} />
        ) : null,
      )}
      {p.impacto ? <EfectoEn efecto={p.impacto} en={ini[ini.length - 1] + 2} volumen={p.sfxVolumen} /> : null}
    </Fondo>
  );
};
