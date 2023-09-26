"""all functions related to Chess.com"""

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

import requests
from tqdm import tqdm

from .date_parser import end_of_month

HEADERS: Dict[str, str] = {
    "User-Agent": "github.com/simske/pgn-downloader pgn-downloader@simske.com"
}


def download_pgn(
    username: str,
    output_path: str,
    color: Optional[str] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    modes: Optional[Iterable[str]] = None,
) -> None:
    """Downloads games and writes them to output file"""

    # Chess.com uses another terminology
    if modes is not None:
        modes = ["daily" if mode == "correspondence" else mode for mode in modes]

    # make `None` datetimes comparable
    if since is None:
        since = datetime.min.replace(tzinfo=timezone.utc)
    if until is None:
        until = datetime.max.replace(tzinfo=timezone.utc)

    r_archives = requests.get(
        f"https://api.chess.com/pub/player/{username}/games/archives", headers=HEADERS
    )
    archives = r_archives.json()["archives"]

    with open(output_path, "x") as f:
        with tqdm(desc="Downloading", unit=" games") as progress:
            for month_url in archives:
                # only download archives in desired time range
                archive_date = datetime.strptime(month_url[-7:], "%Y/%m").replace(
                    tzinfo=timezone.utc
                )
                if end_of_month(archive_date) < since or archive_date > until:
                    continue

                games = requests.get(month_url, headers=HEADERS).json()["games"]

                for game in games:
                    if filter_game(game, username, color, since, until, modes):
                        f.write(game["pgn"] + "\n\n")
                        progress.update(1)


def filter_game(
    game: Dict[str, Any],
    username: str,
    color: Optional[str] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    modes: Optional[Iterable[str]] = None,
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
    if modes is not None:
        select_game &= game["time_class"] in modes

    # select only games played in desired time range
    game_date = datetime.fromtimestamp(game["end_time"]).astimezone(timezone.utc)
    if since is not None:
        select_game &= game_date >= since
    if until is not None:
        select_game &= game_date <= until

    return select_game
