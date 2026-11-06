#!/usr/bin/env python3
"""
G-033 sello.py — Variante --sello para envejecer.py (Cold Case 1987 / 1936).
Aplica ÚNICAMENTE un sello de tinta roja semitransparente ligeramente rotado
con texto configurable ("CASE CLOSED", "CONFIDENTIAL", "CASO CERRADO", etc.)
sobre un PNG existente, sin grano, manchas ni viñeteado.

Uso directo:
  python3 "G-033 sello.py" --input "G-033 certificado-demo-en.png" \
      --output "test_stamped.png" --sello "CASE CLOSED" --angle -14 --alpha 0.72
"""
import argparse
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def encontrar_fuente(size_px: int):
    candidatas = [
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ]
    for path in candidatas:
        try:
            return ImageFont.truetype(path, size_px)
        except OSError:
            continue
    return ImageFont.load_default()


def aplicar_sello_tinta(
    img_path: str,
    out_path: str,
    texto_sello: str = "CASE CLOSED",
    subtexto: str = "BUREAU ARCHIVE • 1987",
    angle: float = -13.5,
    alpha: float = 0.72,
    pos_rel: tuple = (0.76, 0.24),
    seed: int = 1987,
):
    t0 = time.time()
    base = Image.open(img_path).convert("RGBA")
    w, h = base.size

    # Escala proporcional al ancho (a 300 DPI Letter landscape w=3295 px)
    scale = w / 3295.0
    font_main = encontrar_fuente(max(18, int(92 * scale)))
    font_sub = encontrar_fuente(max(12, int(36 * scale)))

    # Medir texto
    dummy = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bbox_main = dummy.textbbox((0, 0), texto_sello.upper(), font=font_main)
    tw_m = bbox_main[2] - bbox_main[0]
    th_m = bbox_main[3] - bbox_main[1]

    bbox_sub = dummy.textbbox((0, 0), subtexto.upper(), font=font_sub)
    tw_s = bbox_sub[2] - bbox_sub[0]
    th_s = bbox_sub[3] - bbox_sub[1]

    pad_x = int(58 * scale)
    pad_y = int(34 * scale)
    box_w = max(tw_m, tw_s) + pad_x * 2
    box_h = th_m + th_s + int(24 * scale) + pad_y * 2

    margin = int(40 * scale)
    stamp = Image.new("RGBA", (box_w + margin * 2, box_h + margin * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(stamp)

    # Color tinta roja de tampón (carmín archivo 1987)
    ink_rgb = (168, 28, 24)
    ink_rgba = (*ink_rgb, int(255 * alpha))

    x0, y0 = margin, margin
    x1, y1 = margin + box_w, margin + box_h
    border_outer = max(3, int(11 * scale))
    border_inner = max(2, int(4 * scale))
    gap = max(3, int(12 * scale))

    # Marco rectangular doble de sello de goma
    draw.rectangle([x0, y0, x1, y1], outline=ink_rgba, width=border_outer)
    draw.rectangle(
        [x0 + gap, y0 + gap, x1 - gap, y1 - gap],
        outline=ink_rgba,
        width=border_inner,
    )

    # Texto principal y subtexto centrados
    tx_m = x0 + (box_w - tw_m) // 2 - bbox_main[0]
    ty_m = y0 + pad_y - bbox_main[1]
    draw.text((tx_m, ty_m), texto_sello.upper(), font=font_main, fill=ink_rgba)

    tx_s = x0 + (box_w - tw_s) // 2 - bbox_sub[0]
    ty_s = ty_m + th_m + int(22 * scale)
    draw.text((tx_s, ty_s), subtexto.upper(), font=font_sub, fill=ink_rgba)

    # Desgaste orgánico de tampón seco (micro-poros en la tinta)
    rng = np.random.default_rng(seed)
    arr = np.array(stamp, dtype=np.float32)
    noise = rng.uniform(0.55, 1.08, size=arr[:, :, 3].shape)
    dropout = (rng.random(size=arr[:, :, 3].shape) > 0.08).astype(np.float32)
    arr[:, :, 3] = np.clip(arr[:, :, 3] * noise * dropout, 0, 255)
    stamp = Image.fromarray(arr.astype(np.uint8), "RGBA")

    # Rotación con bicúbico
    rotated = stamp.rotate(angle, resample=Image.BICUBIC, expand=True)
    rw, rh = rotated.size

    cx = int(w * pos_rel[0]) - rw // 2
    cy = int(h * pos_rel[1]) - rh // 2
    base.alpha_composite(rotated, dest=(max(0, cx), max(0, cy)))

    base.convert("RGB").save(out_path, "PNG", optimize=True)
    dt = time.time() - t0
    print(f"[sello.py] Sello '{texto_sello}' aplicado en {dt:.3f}s -> {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Aplica sello de tinta roja semitransparente (--sello).")
    parser.add_argument("--input", "-i", required=True, help="PNG de entrada")
    parser.add_argument("--output", "-o", required=True, help="PNG de salida")
    parser.add_argument("--sello", "-s", default="CASE CLOSED", help="Texto principal del sello")
    parser.add_argument("--subtexto", default="BUREAU ARCHIVE • 1987", help="Subtexto inferior del sello")
    parser.add_argument("--angle", type=float, default=-13.5, help="Ángulo de rotación en grados")
    parser.add_argument("--alpha", type=float, default=0.72, help="Opacidad de la tinta (0.0 a 1.0)")
    parser.add_argument("--x", type=float, default=0.76, help="Posición horizontal relativa (0-1)")
    parser.add_argument("--y", type=float, default=0.24, help="Posición vertical relativa (0-1)")
    args = parser.parse_args()

    aplicar_sello_tinta(
        img_path=args.input,
        out_path=args.output,
        texto_sello=args.sello,
        subtexto=args.subtexto,
        angle=args.angle,
        alpha=args.alpha,
        pos_rel=(args.x, args.y),
    )


if __name__ == "__main__":
    main()
