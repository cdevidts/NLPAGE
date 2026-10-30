/**
 * Deja el entorno listo. Reanudable: lo que ya está, se salta.
 *
 *   npm run setup
 *
 * 1. Tipografías de Google Fonts a public/fonts/ (solo subsets latin y
 *    latin-ext) y src/fonts.generated.ts. Viven en el repo porque el Chrome del
 *    render no siempre sale a internet (lección de Videos-Next-Layer).
 * 2. Motores de voz y de escucha (Python): piper-tts (voz en español) y
 *    faster-whisper (tiempos de cada palabra y revisión de lo que se oye).
 *    Kokoro (voz en inglés) es un paquete npm y baja su modelo de Hugging Face
 *    la primera vez que se usa.
 * 3. La voz de Piper es_MX-claude-high a .cache/piper/.
 */
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36';

const FAMILIAS =
  'family=Oswald:wght@700&family=Special+Elite&family=Playfair+Display:wght@800&family=Inter:wght@500;800;900';

const fuentes = async () => {
  if (fs.existsSync('src/fonts.generated.ts') && fs.existsSync('public/fonts')) {
    console.log('✓ tipografías');
    return;
  }
  const css = await (await fetch(`https://fonts.googleapis.com/css2?${FAMILIAS}&display=block`, {headers: {'User-Agent': UA}})).text();
  const caras: Array<{family: string; weight: number; file: string; range: string}> = [];
  fs.mkdirSync('public/fonts', {recursive: true});
  for (const m of css.matchAll(/\/\* ([a-z-]+) \*\/\s*@font-face \{([^}]+)\}/g)) {
    if (m[1] !== 'latin' && m[1] !== 'latin-ext') continue;
    const cuerpo = m[2];
    const family = /font-family: '([^']+)'/.exec(cuerpo)![1];
    const weight = Number(/font-weight: (\d+)/.exec(cuerpo)![1]);
    const url = /src: url\(([^)]+)\)/.exec(cuerpo)![1];
    const range = /unicode-range: ([^;]+);/.exec(cuerpo)![1];
    const file = `fonts/${family.replace(/\s+/g, '')}-${weight}-${m[1]}.woff2`;
    fs.writeFileSync(path.join('public', file), Buffer.from(await (await fetch(url)).arrayBuffer()));
    caras.push({family, weight, file, range});
  }
  fs.writeFileSync(
    'src/fonts.generated.ts',
    `// Generado por scripts/setup.ts. No editar a mano.\nexport const FONT_FACES = ${JSON.stringify(caras, null, 1)};\n`,
  );
  console.log(`✓ ${caras.length} archivos de tipografía`);
};

const python = () => {
  const ok = (mod: string) => spawnSync('python3', ['-c', `import ${mod}`]).status === 0;
  const faltan = [ok('piper') ? null : 'piper-tts', ok('faster_whisper') ? null : 'faster-whisper'].filter(Boolean) as string[];
  if (!faltan.length) {
    console.log('✓ piper-tts y faster-whisper');
    return;
  }
  console.log(`… pip install ${faltan.join(' ')}`);
  const r = spawnSync('pip3', ['install', '-q', ...faltan], {stdio: 'inherit'});
  if (r.status !== 0) throw new Error('pip install falló');
};

const piper = async () => {
  const base = 'https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/claude/high/es_MX-claude-high';
  const dir = '.cache/piper';
  fs.mkdirSync(dir, {recursive: true});
  for (const ext of ['.onnx', '.onnx.json']) {
    const destino = path.join(dir, `es_MX-claude-high${ext}`);
    if (fs.existsSync(destino) && fs.statSync(destino).size > 1000) continue;
    const r = await fetch(base + ext);
    if (!r.ok) throw new Error(`voz de Piper: HTTP ${r.status}`);
    fs.writeFileSync(destino, Buffer.from(await r.arrayBuffer()));
  }
  console.log('✓ voz Piper es_MX-claude-high');
};

await fuentes();
python();
await piper();
console.log('\nListo. Siguiente: npm run producto -- <carpeta de etsy/>');
