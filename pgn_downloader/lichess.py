"""all functions related to lichess"""

from datetime import datetime, timezone
from os import PathLike
from typing import Dict, Iterable, List, Optional, Union

import requests
from tqdm import tqdm  # type: ignore

LICHESS_ENDPOINT = "https://lichess.org/api"


def download_pgn(
    username: str,
    output_path: Union[str, PathLike[str]],
    color: Optional[str] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    modes: Optional[Iterable[str]] = None,
) -> None:
    """Download PGN from lichess with specified filters"""
    url = f"{LICHESS_ENDPOINT}/games/user/{username}"

    # set parameters for api
    params: Dict[str, Union[str, int]] = {"sort": "dateAsc"}
    if since is not None:
        # timestamps in milliseconds
        params["since"] = int(since.astimezone(timezone.utc).timestamp() * 1000)
    if until is not None:
        params["until"] = int(until.astimezone(timezone.utc).timestamp() * 1000)
    if color is not None:
        params["color"] = color
    if modes is not None:
        params["perfType"] = ",".join(modes)

    with requests.get(url, params=params, stream=True) as r:
        r.raise_for_status()
        last_prev = b"x"  # tmp variable to store last byte of each chunk
        with open(output_path, "xb") as f:
            with tqdm(desc="Downloading", unit=" games") as progress:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    # count games in chunk by counting double newlines
                    # which indicate start of next pgn
                    # last_prev checks for newline at chunk boundary
                    progress.update(
                        chunk.count(b"\n\n")
                        + int(last_prev == b"\n" and chunk[0] == b"\n")
                    )
                    last_prev = chunk[-1]
