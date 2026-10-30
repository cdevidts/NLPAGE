/**
 * Prepara el material de un producto de la tienda para sus videos.
 *
 *   npm run producto -- 56-cold-case-01
 *
 * Copia las fotos del listing y convierte cada PDF (menos las soluciones, que
 * no se muestran nunca) en una imagen por página, a public/productos/<carpeta>/.
 * Deja una hoja de contacto por PDF en out/productos/<carpeta>/ con el número
 * de cada página: ábrela antes de escribir el plan y elige páginas mirando,
 * no adivinando.
 */
import fs from 'node:fs';
import path from 'node:path';
import {ETSY_DIR, sh} from './lib/comun';

const HOJA = String.raw`
import sys, os
from PIL import Image, ImageDraw, ImageFont
d, out = sys.argv[1], sys.argv[2]
fs = sorted(f for f in os.listdir(d) if f.endswith('.jpg'))
w, h, cols = 220, 285, 8
rows = (len(fs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, rows * (h + 34)), 'white')
dr = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
except Exception: font = ImageFont.load_default()
for i, f in enumerate(fs):
    im = Image.open(os.path.join(d, f)).convert('RGB'); im.thumbnail((w - 8, h - 4))
    x, y = (i % cols) * w, (i // cols) * (h + 34)
    sheet.paste(im, (x + 4, y + 34)); dr.text((x + 8, y + 2), str(int(f[:-4])), fill='red', font=font)
sheet.save(out, quality=82)
`;

const carpeta = process.argv[2];
if (!carpeta) throw new Error('Uso: npm run producto -- <carpeta de etsy/>');
const origen = path.join(ETSY_DIR, carpeta);
if (!fs.existsSync(origen)) throw new Error(`No existe ${origen}`);

const destino = path.join('public/productos', carpeta);
const hojas = path.join('out/productos', carpeta);
fs.mkdirSync(path.join(destino, 'fotos'), {recursive: true});
fs.mkdirSync(hojas, {recursive: true});

const fotos = fs.readdirSync(origen).filter((f) => /^\d\d\.jpg$/.test(f)).sort();
for (const f of fotos) fs.copyFileSync(path.join(origen, f), path.join(destino, 'fotos', f));
console.log(`✓ ${fotos.length} fotos del listing → ${destino}/fotos/  (atajo "foto:01")`);

const pdfs = fs
  .readdirSync(origen)
  .filter((f) => f.toLowerCase().endsWith('.pdf') && !/solu(tion|cion|ción)/i.test(f))
  .sort();
const indice: Record<string, {pdf: string; paginas: number}> = {};
pdfs.forEach((pdf, i) => {
  // "-EN-ES.pdf" (sobres sellados bilingües) no puede pisar las páginas de "-ES.pdf".
  const m = /-(EN-ES|EN|ES)\.pdf$/i.exec(pdf);
  const alias = m ? m[1].toLowerCase().replace('-', '') : String(i + 1);
  const dir = path.join(destino, `paginas-${alias}`);
  const info = sh('pdfinfo', [path.join(origen, pdf)], {silencio: true});
  const n = Number(/Pages:\s+(\d+)/.exec(info)?.[1] ?? 0);
  if (n < 2) return; // los PDF de una página son solo el link de entrega
  fs.mkdirSync(dir, {recursive: true});
  if (fs.readdirSync(dir).length < n) {
    sh('pdftoppm', ['-jpeg', '-jpegopt', 'quality=88', '-scale-to-y', '2200', '-scale-to-x', '-1', path.join(origen, pdf), path.join(dir, 'p')]);
    for (const f of fs.readdirSync(dir)) {
      const k = /^p-0*(\d+)\.jpg$/.exec(f);
      if (k) fs.renameSync(path.join(dir, f), path.join(dir, `${k[1].padStart(2, '0')}.jpg`));
    }
  }
  indice[alias] = {pdf, paginas: n};
  // Hoja de contacto con el número de cada página.
  const hoja = path.join(hojas, `HOJA-${alias}.jpg`);
  sh('python3', ['-I', '-c', HOJA, dir, hoja], {silencio: true});
  console.log(`✓ ${pdf}: ${n} páginas → paginas-${alias}/  (atajo "pag:${alias}:7")  hoja: ${hoja}`);
});
fs.writeFileSync(path.join(destino, 'indice.json'), JSON.stringify({fotos, pdfs: indice}, null, 1));

const listing = ['LISTING.txt', 'listing_data.py'].find((f) => fs.existsSync(path.join(origen, f)));
if (listing) console.log(`\nCopy del listing (para el guion): ${path.join(origen, listing)}`);

