# outlinelab

Conversor open source de imagens raster (PNG, JPG, WebP) para vetor SVG.

Status: **núcleo inicial**. Traça contornos por cor com paleta reduzida ou modo preto e branco.

## Instalação

Requer Python 3.10 a 3.13. Testado com 3.11. Com 3.14, `vtracer` 0.6.15 derruba o processo (segfault no Windows).

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows
pip install -e ".[dev]"
```

## Uso

```bash
outlinelab logo.png -o logo.svg --colors 6
outlinelab desenho.jpg --bw
outlinelab foto.png --original-colors
```

Opções:

- `-o, --output`: SVG de saída (padrão: mesmo nome com `.svg`).
- `-c, --colors`: máximo de cores da paleta antes do traçado (padrão: 8).
- `--original-colors`: não reduz a paleta.
- `--bw`: preto e branco por limiar Otsu.

Transparência é composta sobre fundo branco.

## Testes

```bash
pytest
```

## Dependências

- [vtracer](https://github.com/visioncortex/vtracer) (MIT): traçado raster → vetor.
- OpenCV, NumPy, Pillow: pré-processamento e quantização.

## Roteiro

- Exportação PDF, EPS e DXF.
- Remoção de fundo.
- Controle de cantos e edição por região.
- Interface web.

## Licença

MIT. Veja [LICENSE](LICENSE).
