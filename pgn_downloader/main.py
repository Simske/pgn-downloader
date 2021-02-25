#!/usr/bin/env python3
import argparse

import requests

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
            f"{args.username}.pgn"
        else:
            f"{args.username}-{args.color}.pgn"

    return args


def download_pgn(username: str, color=None):
    """Downloads games and concatenates pgn to string"""
    print(
        f"Loading Games for user {username}"
        f"{ 'with color {color} ' if color else '' }on chess.com"
    )

    r_archives = requests.get(
        f"https://api.chess.com/pub/player/{username}/games/archives"
    )
    archives = r_archives.json()["archives"]

    pgn = ""
    nr_games = 0
    for month_url in archives:
        print(f"Downloading games from {month_url[-7:]}", end="\r")
        games = requests.get(month_url).json()["games"]

        for game in games:
            if filter_game(game, username, color):
                pgn += game["pgn"] + "\n\n"
                nr_games += 1

    print(f"\nDownloaded {nr_games} games")
    return pgn


def filter_game(game: dict, username: str, color: str = None) -> bool:
    """Decide if game should be downloaded.

    Args:
        game (dict): game over which to decide
        username (str): username of player (needed for color selection)
        color (:obj:`str`, optional): player color to select.
            Choices are `None`(for all colors), `white`, `black`.
            Defaults to `None`

    Returns:
        bool: if game is selected

    """
    # return value, all checks should or with this
    select_game: bool = True

    # check if pgn even exists
    if "pgn" not in game:
        select_game &= False

    if color is not None:
        select_game &= game[color]["username"] == username

    return select_game


def cli_entrypoint():
    args = cli_arguments()
    pgn = download_pgn(args.username, args.color)

    with open(args.output, "w") as f:
        f.write(pgn)

    print(f"Saved pgn to {args.output}")


if __name__ == "__main__":
    cli_entrypoint()
