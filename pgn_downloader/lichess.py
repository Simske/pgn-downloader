"""all functions related to lichess"""

from datetime import datetime, timezone

import requests

LICHESS_ENDPOINT = "https://lichess.org/api"


def download_pgn(
    username: str,
    output_path,
    color: str = None,
    since: datetime = None,
    until: datetime = None,
    modes: list = None,
):
    """Download PGN from lichess with specified filters"""
    url = f"{LICHESS_ENDPOINT}/games/user/{username}"
    params = {}
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
        with open(output_path, "xb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
