#!/usr/bin/env python3
import argparse

from . import chess_com, lichess
from .version import version


def cli_arguments(args=None):
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"%(prog)s {version}")
    parser.add_argument(
        "server", choices=("chess.com", "lichess"), help="Server to download games from"
    )
    # TODO: time format
    parser.add_argument("username", help="Username on chosen server")
    parser.add_argument(
        "--since", help="Download games since (default: account creation)"
    )
    parser.add_argument("--until", help="Download games until (default: now)")
    parser.add_argument(
        "--mode",
        default="blitz,rapid,classical,correspondence",
        help="Game mode which will be downloaded. Comma separated list "
        "(default: blitz,rapid,classical,correspondence)",
    )
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
            args.output = f"{args.server}_{args.username}.pgn"
        else:
            args.output = f"{args.server}_{args.username}-{args.color}.pgn"

    # parse playing modes
    args.mode = args.mode.split(",")

    return args


def main():
    args = cli_arguments()

    if args.server == "chess.com":
        print("Filters other than color are not implemented for chess.com")
        pgn = chess_com.download_pgn(args.username, args.color)

        with open(args.output, "x") as f:
            f.write(pgn)

        print(f"Saved pgn to {args.output}")
    elif args.server == "lichess":
        print("Not all filters are implemented yet!")
        lichess.download_pgn(
            args.username, args.output, color=args.color, modes=args.mode
        )
        print("Downloaded games from Lichess")


if __name__ == "__main__":
    main()
