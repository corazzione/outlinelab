"""Interface de linha de comando."""

from __future__ import annotations

import argparse
import sys

from outlinelab.core import vectorize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="outlinelab",
        description="Converte imagens raster (PNG, JPG, WebP) em SVG.",
    )
    parser.add_argument("input", help="imagem de entrada")
    parser.add_argument("-o", "--output", help="SVG de saída (padrão: entrada com .svg)")
    parser.add_argument(
        "-c",
        "--colors",
        type=int,
        default=8,
        help="número máximo de cores da paleta (padrão: 8)",
    )
    parser.add_argument(
        "--original-colors",
        action="store_true",
        help="não reduz a paleta; traça as cores originais",
    )
    parser.add_argument(
        "--bw",
        action="store_true",
        help="preto e branco (limiar Otsu), ignora --colors",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = args.output or args.input.rsplit(".", 1)[0] + ".svg"
    mode = "bw" if args.bw else "color"
    n_colors = None if args.original_colors else args.colors

    try:
        path = vectorize(args.input, output, n_colors=n_colors, mode=mode)
    except (OSError, ValueError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1

    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
