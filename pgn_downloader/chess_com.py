"""all functions related to Chess.com"""

from datetime import datetime

import requests


def download_pgn(
    username: str,
    output_path,
    color: str = None,
    since: datetime = None,
    until: datetime = None,
    modes: list = None,
):
    """Downloads games and writes them to output file"""
    print(
        f"Loading Games for user {username}"
        f"{ 'with color {color} ' if color else '' } on chess.com"
    )

    # Chess.com uses another terminology
    for i in range(len(modes)):
        modes[i] = modes[i].replace("correspondence", "daily")

    r_archives = requests.get(
        f"https://api.chess.com/pub/player/{username}/games/archives"
    )
    archives = r_archives.json()["archives"]

    nr_games = 0
    with open(output_path, "w") as f:
        for month_url in archives:
            # only download archives in desired time range
            archive_date = datetime.strptime(month_url[-7:], "%Y/%m")
            if since is not None:
                if too_old(archive_date, since):
                    continue
            if until is not None:
                if too_young(archive_date, until):
                    continue
            print(f"Downloading games from {month_url[-7:]}", end="\r")
            games = requests.get(month_url).json()["games"]

            for game in games:
                if filter_game(game, username, color, since, until, modes):
                    f.write(game["pgn"] + "\n\n")
                    nr_games += 1

        print(f"\nDownloaded {nr_games} games")


def filter_game(
    game: dict,
    username: str,
    color: str = None,
    since: datetime = None,
    until: datetime = None,
    modes: list = None,
) -> bool:
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

    # exclude Chess960 and other variants
    select_game &= game["rules"] == "chess"
    # select only games where user is playing with desired color
    if color is not None:
        select_game &= game[color]["username"] == username

    # select only desired time controls
    select_game &= game["time_class"] in modes

    # select only games played in desired time range
    game_date = datetime.fromtimestamp(game["end_time"]).astimezone()

    if since is not None:
        select_game &= game_date >= since

    if until is not None:
        select_game &= game_date <= until

    return select_game


def too_young(archive_date: datetime, until: datetime) -> bool:
    """check if archive date is newer than until, disregarding days"""
    if archive_date.year > until.year or (
        archive_date.year == until.year and archive_date.month > until.month
    ):
        return True
    else:
        return False


def too_old(archive_date: datetime, since: datetime) -> bool:
    """check if archive date is older than since, disregarding days"""
    if archive_date.year < since.year or (
        archive_date.year == since.year and archive_date.month < since.month
    ):
        return True
    else:
        return False
