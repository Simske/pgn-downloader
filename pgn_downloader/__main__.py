import argparse
import sys

from . import chess_com, lichess
from .date_parser import parse_date
from .version import version


def cli_arguments() -> argparse.Namespace:
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "server", choices=("chess.com", "lichess"), help="Server to download games from"
    )
    parser.add_argument("username", help="Username on chosen server")
    parser.add_argument(
        "-c",
        "--color",
        default=None,
        choices=["white", "black"],
        help="Color (white/black) (default: both)",
    )
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
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output filename (default: server_username-color.pgn)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {version}")

    args = parser.parse_args()

    ## Post-process arguments
    # generate output filename default
    if args.output is None:
        if args.color is None:
            args.output = f"{args.server}_{args.username}.pgn"
        else:
            args.output = f"{args.server}_{args.username}-{args.color}.pgn"

    # parse playing modes
    args.mode = args.mode.split(",")

    # parse `since` and `until` date strings
    if args.since is not None:
        args.since = parse_date(args.since)
    if args.until is not None:
        args.until = parse_date(args.until, end=True)

    return args


def main() -> None:
    try:
        args = cli_arguments()

        print(
            f"pgn-downloader {version}\n"
            f"Downloading games for user '{args.username}' from {args.server}\n"
            "Filters:\n"
            f"    Color: {args.color if args.color is not None else 'both'}\n"
            "    Date: since "
            f"{args.since.isoformat(' ') if args.since is not None else 'Account creation'}"
            f" until {args.until.isoformat(' ') if args.until is not None else 'now'}\n"
            f"    Modes: {', '.join(args.mode)}"
        )

        if args.server == "chess.com":
            chess_com.download_pgn(
                args.username,
                args.output,
                color=args.color,
                modes=args.mode,
                since=args.since,
                until=args.until,
            )

        elif args.server == "lichess":
            lichess.download_pgn(
                args.username,
                args.output,
                color=args.color,
                modes=args.mode,
                since=args.since,
                until=args.until,
            )

        print(f"Saved games to {args.output}")

    except Exception as e:
        print("\nAn Error occured: ")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
