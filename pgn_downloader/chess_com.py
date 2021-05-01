"""all functions related to Chess.com"""

import requests


def download_pgn(username: str, color=None):
    """Downloads games and concatenates pgn to string"""
    print(
        f"Loading Games for user {username}"
        f"{ 'with color {color} ' if color else '' } on chess.com"
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
