"""Núcleo: reduz a paleta da imagem e traça os contornos em SVG."""

from __future__ import annotations

import tempfile
from pathlib import Path

import cv2
import numpy as np
import vtracer
from PIL import Image

Mode = str  # "color" | "bw"


def load_rgb(path: str | Path) -> np.ndarray:
    """Abre a imagem e devolve RGB uint8. Transparência vira fundo branco."""
    with Image.open(path) as img:
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            rgba = img.convert("RGBA")
            background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
            img = Image.alpha_composite(background, rgba)
        return np.asarray(img.convert("RGB"))


def quantize(rgb: np.ndarray, n_colors: int, attempts: int = 3) -> np.ndarray:
    """Reduz a imagem a no máximo `n_colors` cores via k-means."""
    if n_colors < 1:
        raise ValueError("n_colors deve ser >= 1")

    pixels = rgb.reshape(-1, 3).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(
        pixels, n_colors, None, criteria, attempts, cv2.KMEANS_PP_CENTERS
    )
    palette = np.clip(centers, 0, 255).astype(np.uint8)
    return palette[labels.flatten()].reshape(rgb.shape)


def vectorize(
    input_path: str | Path,
    output_path: str | Path,
    n_colors: int | None = 8,
    mode: Mode = "color",
) -> Path:
    """Converte a imagem em SVG e devolve o caminho escrito.

    n_colors: tamanho máximo da paleta antes do traçado. None mantém as cores originais.
    mode: "color" (traça por cor) ou "bw" (preto e branco).
    """
    if mode not in ("color", "bw"):
        raise ValueError(f"modo inválido: {mode!r}")

    rgb = load_rgb(input_path)
    if mode == "bw":
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    elif n_colors is not None:
        rgb = quantize(rgb, n_colors)

    output_path = Path(output_path)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_png = Path(tmp) / "input.png"
        Image.fromarray(rgb).save(tmp_png)
        vtracer.convert_image_to_svg_py(
            str(tmp_png),
            str(output_path),
            colormode="binary" if mode == "bw" else "color",
            mode="spline",
            hierarchical="stacked",
        )
    return output_path
