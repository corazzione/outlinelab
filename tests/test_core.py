import numpy as np
import pytest
from PIL import Image

from outlinelab.cli import main
from outlinelab.core import quantize, vectorize


@pytest.fixture
def shapes_png(tmp_path):
    """Imagem sintética: fundo branco, quadrado vermelho, círculo azul."""
    img = Image.new("RGB", (120, 120), (255, 255, 255))
    arr = np.asarray(img).copy()
    arr[10:50, 10:50] = (220, 30, 30)
    yy, xx = np.ogrid[:120, :120]
    circle = (xx - 85) ** 2 + (yy - 85) ** 2 <= 25**2
    arr[circle] = (30, 60, 220)
    path = tmp_path / "shapes.png"
    Image.fromarray(arr).save(path)
    return path


def test_quantize_limits_palette():
    rng = np.random.default_rng(0)
    rgb = rng.integers(0, 256, size=(64, 64, 3), dtype=np.uint8)
    out = quantize(rgb, n_colors=4)
    assert out.shape == rgb.shape
    assert len(np.unique(out.reshape(-1, 3), axis=0)) <= 4


def test_quantize_rejects_zero_colors():
    with pytest.raises(ValueError):
        quantize(np.zeros((2, 2, 3), dtype=np.uint8), n_colors=0)


def test_vectorize_writes_svg(shapes_png, tmp_path):
    out = vectorize(shapes_png, tmp_path / "out.svg", n_colors=4)
    text = out.read_text(encoding="utf-8")
    assert "<svg" in text
    assert "<path" in text


def test_vectorize_bw(shapes_png, tmp_path):
    out = vectorize(shapes_png, tmp_path / "bw.svg", mode="bw")
    assert "<svg" in out.read_text(encoding="utf-8")


def test_vectorize_rejects_unknown_mode(shapes_png, tmp_path):
    with pytest.raises(ValueError):
        vectorize(shapes_png, tmp_path / "x.svg", mode="cmyk")


def test_cli_default_output_name(shapes_png):
    assert main([str(shapes_png), "--colors", "4"]) == 0
    assert shapes_png.with_suffix(".svg").exists()


def test_cli_missing_input_returns_error(tmp_path, capsys):
    assert main([str(tmp_path / "nope.png")]) == 1
    assert "erro" in capsys.readouterr().err
