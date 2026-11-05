#!/usr/bin/env python3
"""
G-030 envejecer.py
Aplica envejecido de periódico de archivo (1987) sobre un PNG a 300 DPI usando solo Pillow y NumPy:
- Amarilleo regulable (0.0 a 1.0)
- Grano de papel prensa e imperfecciones de fibra
- Viñeteado perimetral por oxidación del papel
- 1 a 3 manchas de café con borde oscuro (anillo capilar)
- Doblez horizontal con sombra y desgaste de tinta en el pliegue
- Borde irregular rasgado o cortado con tijera
- Leve desaturación y ablandamiento del negro de la tinta
"""

import argparse
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def crear_mascara_mancha_cafe(h, w, rng, cx, cy, radio_base):
    """Genera una mancha de café orgánica con anillo capilar más oscuro en el borde."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ang = np.arctan2(yy - cy, xx - cx)
    # Deformación radial armónica para contorno orgánico
    deform = np.zeros_like(ang)
    for k in range(2, 8):
        amp = rng.uniform(0.03, 0.11) / (k * 0.45)
        fase = rng.uniform(0, 2 * np.pi)
        deform += amp * np.cos(k * ang + fase)
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / (radio_base * (1.0 + deform))

    # Interior suave + anillo concentrado cerca de dist ~ 0.88 - 1.02
    interior = np.clip(1.0 - dist ** 2.2, 0.0, 1.0) * 0.42
    anillo = np.exp(-((dist - 0.93) / 0.075) ** 2) * 0.85
    salpicadura = np.exp(-((dist - 1.08) / 0.035) ** 2) * (rng.random((h, w)) > 0.72) * 0.35

    mascara = np.clip(interior + anillo + salpicadura, 0.0, 1.0)
    # Suavizado ligero con Pillow para evitar bordes pixelados
    img_m = Image.fromarray((mascara * 255).astype(np.uint8), mode="L")
    img_m = img_m.filter(ImageFilter.GaussianBlur(radius=2.2))
    return np.asarray(img_m, dtype=np.float32) / 255.0


def crear_mascara_borde(h, w, rng, modo="tijera", margen=28):
    """Crea máscara alfa con corte irregular de tijera y una esquina rasgada."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    def perfil_1d(n, amplitud, paso):
        nodos = max(4, n // paso)
        vals = rng.normal(0.0, amplitud, size=nodos)
        x_nodos = np.linspace(0, n - 1, nodos)
        return np.interp(np.arange(n), x_nodos, vals)

    if modo == "tijera":
        # Trazos poligonales largos de tijera con leves cambios de ángulo
        top = margen + perfil_1d(w, 4.5, 180) + perfil_1d(w, 1.2, 35)
        bottom = (h - margen) + perfil_1d(w, 5.0, 170) + perfil_1d(w, 1.4, 30)
        left = margen + perfil_1d(h, 4.5, 190) + perfil_1d(h, 1.2, 35)
        right = (w - margen) + perfil_1d(h, 5.0, 165) + perfil_1d(h, 1.5, 30)
    else:
        # Borde rasgado fibroso
        top = margen + perfil_1d(w, 9.0, 90) + perfil_1d(w, 3.5, 14) + perfil_1d(w, 1.5, 4)
        bottom = (h - margen) + perfil_1d(w, 10.0, 85) + perfil_1d(w, 3.8, 12) + perfil_1d(w, 1.6, 4)
        left = margen + perfil_1d(h, 8.5, 95) + perfil_1d(h, 3.2, 14) + perfil_1d(h, 1.4, 4)
        right = (w - margen) + perfil_1d(h, 9.5, 85) + perfil_1d(h, 3.6, 12) + perfil_1d(h, 1.5, 4)

    mask = (
        (yy >= top[None, :])
        & (yy <= bottom[None, :])
        & (xx >= left[:, None])
        & (xx <= right[:, None])
    ).astype(np.float32)

    # Pequeña muesca/rasgado diagonal en la esquina inferior derecha
    corte_esq = (xx - (w - 95)) * 0.78 + (yy - (h - 75)) * 1.0 + perfil_1d(w, 3.2, 12)[None, :]
    mask = np.where(corte_esq > 32, 0.0, mask)

    img_alpha = Image.fromarray((mask * 255).astype(np.uint8), mode="L")
    img_alpha = img_alpha.filter(ImageFilter.GaussianBlur(radius=0.85))
    return np.asarray(img_alpha, dtype=np.float32) / 255.0


def envejecer_recorte(
    input_path: str,
    output_path: str,
    amarilleo: float = 0.58,
    grano: float = 0.055,
    vineteado: float = 0.32,
    manchas: int = 2,
    pos_doblez: float = 0.48,
    intensidad_doblez: float = 0.38,
    desaturacion_tinta: float = 0.18,
    modo_borde: str = "tijera",
    seed: int = 1987,
):
    rng = np.random.default_rng(seed)
    base_img = Image.open(input_path).convert("RGB")
    # Leve ablandamiento óptico propio de prensa rotativa offset de 1987
    base_img = base_img.filter(ImageFilter.GaussianBlur(radius=0.35))
    arr = np.asarray(base_img, dtype=np.float32) / 255.0
    h, w, _ = arr.shape

    # 1. Desaturación y levantamiento del negro de la tinta (carbón envejecido)
    luma = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    arr = arr * (1.0 - desaturacion_tinta) + luma[:, :, None] * desaturacion_tinta
    negro_min = 0.11 * desaturacion_tinta * 2.2
    arr = negro_min + arr * (1.0 - negro_min * 0.85)

    # 2. Amarilleo de papel prensa (tono cálido ocre/crema proporcional a amarilleo 0-1)
    a = float(np.clip(amarilleo, 0.0, 1.0))
    tono_papel = np.array([
        1.0 - 0.05 * a,   # R ligeramente cálido
        1.0 - 0.14 * a,   # G atenuado
        1.0 - 0.34 * a,   # B fuertemente reducido por oxidación de lignina
    ], dtype=np.float32)
    arr = arr * tono_papel[None, None, :]

    # Variación de manchas de humedad suaves (foxing de baja frecuencia)
    baja_h, baja_w = max(8, h // 48), max(8, w // 48)
    ruido_bajo = rng.normal(0.0, 1.0, size=(baja_h, baja_w)).astype(np.float32)
    img_bajo = Image.fromarray(
        np.clip((ruido_bajo * 0.22 + 0.5) * 255, 0, 255).astype(np.uint8), mode="L"
    ).resize((w, h), resample=Image.Resampling.BICUBIC)
    mapa_foxing = (np.asarray(img_bajo, dtype=np.float32) / 255.0 - 0.5) * (0.14 * a)
    arr[:, :, 0] += mapa_foxing * 0.7
    arr[:, :, 1] += mapa_foxing * 0.45
    arr[:, :, 2] -= np.abs(mapa_foxing) * 0.6

    # 3. Viñeteado perimetral por oxidación en los bordes del recorte
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = (xx / (w - 1.0)) * 2.0 - 1.0
    ny = (yy / (h - 1.0)) * 2.0 - 1.0
    dist_borde = np.maximum(np.abs(nx) ** 2.4, np.abs(ny) ** 2.4)
    rad = np.clip((nx ** 2 + ny ** 2) * 0.65 + dist_borde * 0.55, 0.0, 1.5)
    factor_vin = 1.0 - vineteado * (rad ** 1.35)
    arr[:, :, 0] *= np.clip(factor_vin + 0.03 * vineteado, 0.55, 1.0)
    arr[:, :, 1] *= np.clip(factor_vin - 0.02 * vineteado, 0.48, 1.0)
    arr[:, :, 2] *= np.clip(factor_vin - 0.08 * vineteado, 0.38, 1.0)

    # 4. Manchas de café (1 a 3 manchas con borde oscuro capilar)
    n_manchas = int(np.clip(manchas, 0, 3))
    centros_Candidatos = [
        (w * 0.78, h * 0.24, min(w, h) * 0.16),
        (w * 0.22, h * 0.79, min(w, h) * 0.13),
        (w * 0.68, h * 0.72, min(w, h) * 0.11),
    ]
    color_cafe = np.array([0.46, 0.31, 0.16], dtype=np.float32)
    for idx in range(n_manchas):
        cx, cy, r_base = centros_Candidatos[idx]
        cx += rng.uniform(-35, 35)
        cy += rng.uniform(-35, 35)
        m_cafe = crear_mascara_mancha_cafe(h, w, rng, cx, cy, r_base) * 0.52
        arr = arr * (1.0 - m_cafe[:, :, None]) + (arr * color_cafe[None, None, :]) * m_cafe[:, :, None]

    # 5. Doblez horizontal con sombra y línea de desgaste de fibra
    y_fold = int(h * pos_doblez)
    onda_pliegue = np.sin(np.linspace(0, 3.2 * np.pi, w)) * 3.5
    dy = yy - (y_fold + onda_pliegue[None, :])
    # Sombra ancha debajo del pliegue y cresta iluminada/desgastada justo encima
    sombra_pliegue = np.exp(-((dy - 9.0) / 16.0) ** 2) * (0.22 * intensidad_doblez)
    cresta_pliegue = np.exp(-((dy + 2.0) / 3.2) ** 2) * (0.26 * intensidad_doblez)
    arr = arr * (1.0 - sombra_pliegue[:, :, None])
    # En la arista del doblez la tinta se quiebra y asoma la fibra clara del papel
    color_fibra = np.array([0.92, 0.86, 0.72], dtype=np.float32)
    arr = arr * (1.0 - cresta_pliegue[:, :, None]) + color_fibra[None, None, :] * cresta_pliegue[:, :, None]

    # 6. Grano de papel prensa y microfibras
    ruido_grano = rng.normal(0.0, grano, size=(h, w)).astype(np.float32)
    # Fibras cortas horizontales/verticales
    fibras = rng.normal(0.0, grano * 0.55, size=(h // 2, w // 4)).astype(np.float32)
    img_fib = Image.fromarray(
        np.clip((fibras * 4.0 + 0.5) * 255, 0, 255).astype(np.uint8), mode="L"
    ).resize((w, h), resample=Image.Resampling.BILINEAR)
    arr_fib = (np.asarray(img_fib, dtype=np.float32) / 255.0 - 0.5) * (grano * 0.9)
    delta_grano = ruido_grano + arr_fib
    arr += delta_grano[:, :, None]

    arr = np.clip(arr, 0.0, 1.0)

    # 7. Borde irregular cortado/rasgado con sombra proyectada sobre mesa neutra oscura
    alpha_mask = crear_mascara_borde(h, w, rng, modo=modo_borde, margen=26)
    # Oscurecimiento leve en los 6 px inmediatos al corte por oxidación del canto
    img_inner = Image.fromarray((alpha_mask * 255).astype(np.uint8), mode="L")
    img_inner_blur = img_inner.filter(ImageFilter.GaussianBlur(radius=5.0))
    borde_oxido = np.clip(alpha_mask - (np.asarray(img_inner_blur, dtype=np.float32) / 255.0), 0.0, 1.0)
    arr *= (1.0 - borde_oxido[:, :, None] * 0.28)

    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[:, :, :3] = (np.clip(arr, 0.0, 1.0) * 255).astype(np.uint8)
    rgba[:, :, 3] = (np.clip(alpha_mask, 0.0, 1.0) * 255).astype(np.uint8)

    out_img = Image.fromarray(rgba, mode="RGBA")
    # Cuantización adaptativa de 256 colores con canal alfa preservado para mantener el PNG < 2.5 MB a 300 DPI
    out_q = out_img.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
    out_q.save(output_path, format="PNG", dpi=(300, 300), optimize=True, compress_level=9)


def main():
    parser = argparse.ArgumentParser(description="Envejecedor de recortes de prensa (1987) a 300 DPI.")
    parser.add_argument("input_png", help="Ruta del PNG limpio a 300 DPI")
    parser.add_argument("output_png", help="Ruta del PNG envejecido de salida")
    parser.add_argument("--amarilleo", type=float, default=0.58, help="Intensidad de amarilleo (0.0 a 1.0)")
    parser.add_argument("--grano", type=float, default=0.055, help="Intensidad de grano de papel (default: 0.055)")
    parser.add_argument("--vineteado", type=float, default=0.32, help="Viñeteado perimetral (default: 0.32)")
    parser.add_argument("--manchas", type=int, default=2, help="Cantidad de manchas de café (1 a 3, default: 2)")
    parser.add_argument("--pos-doblez", type=float, default=0.48, help="Posición vertical del doblez (0-1, default: 0.48)")
    parser.add_argument("--intensidad-doblez", type=float, default=0.38, help="Intensidad de sombra del doblez (default: 0.38)")
    parser.add_argument("--desaturacion", type=float, default=0.18, help="Desaturación/desgaste de tinta (default: 0.18)")
    parser.add_argument("--borde", choices=["tijera", "rasgado"], default="tijera", help="Estilo del borde exterior")
    parser.add_argument("--seed", type=int, default=1987, help="Semilla reproducible (default: 1987)")
    args = parser.parse_args()

    t0 = time.perf_counter()
    envejecer_recorte(
        input_path=args.input_png,
        output_path=args.output_png,
        amarilleo=args.amarilleo,
        grano=args.grano,
        vineteado=args.vineteado,
        manchas=args.manchas,
        pos_doblez=args.pos_doblez,
        intensidad_doblez=args.intensidad_doblez,
        desaturacion_tinta=args.desaturacion,
        modo_borde=args.borde,
        seed=args.seed,
    )
    dt = time.perf_counter() - t0
    print(f"OK: '{args.output_png}' generado en {dt:.3f} s")


if __name__ == "__main__":
    main()
