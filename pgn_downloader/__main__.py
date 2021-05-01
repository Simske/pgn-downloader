#!/usr/bin/env python3
import argparse

from . import chess_com
from .version import version


def cli_arguments(args=None):
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"%(prog)s {version}")
    parser.add_argument("username")
    parser.add_argument("-o", "--output", default=None, help="Output filename")
    parser.add_argument(
        "-c",
        "--color",
        default=None,
        choices=["white", "black"],
        help="Color (white/black)",
    )

    args = parser.parse_args()
    # generate output filename default
    if args.output is None:
        if args.color is None:
            args.output = f"{args.username}.pgn"
        else:
            args.output = f"{args.username}-{args.color}.pgn"

    return args


def main():
    args = cli_arguments()
    pgn = chess_com.download_pgn(args.username, args.color)

    with open(args.output, "x") as f:
        f.write(pgn)

    print(f"Saved pgn to {args.output}")


if __name__ == "__main__":
    main()
