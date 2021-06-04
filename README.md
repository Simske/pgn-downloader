# pgn-downloader

`pgn-downloader` is a CLI tool to download chess games from [Lichess](https://lichess.org) or [chess.com](https://chess.com).

It provides filters to specify playing color, date range and playing mode.

## Installation
`pgn-downloader` requires Python >=3.6.

It can then installed with `pip`:
```
pip install --upgrade pgn-downloader
```

With this the tool can started with either:
```
pgn-downloader server username
python -m pgn_downloader server username
```

## Usage
```
usage: pgn-downloader [-h] [-c {white,black}] [--since SINCE] [--until UNTIL] [--mode MODE] [-o OUTPUT] [--version] {chess.com,lichess} username

positional arguments:
  {chess.com,lichess}   Server to download games from
  username              Username on chosen server

optional arguments:
  -h, --help            show this help message and exit
  -c {white,black}, --color {white,black}
                        Color (white/black) (default: both)
  --since SINCE         Download games since (default: account creation)
  --until UNTIL         Download games until (default: now)
  --mode MODE           Game mode which will be downloaded. Comma separated list (default: blitz,rapid,classical,correspondence)
  -o OUTPUT, --output OUTPUT
                        Output filename (default: server_username-color.pgn)
  --version             show program's version number and exit
```

Games can be downloaded from either chess.com or lichess.org.
If desired the download can be restricted to a certain color, time control and date range.

The time control is specified as a comma-seperated list, with the default `blitz,rapid,classical,correspondence`.
The possible values are:
- for Lichess: `ultraBullet`, `bullet`, `blitz`, `rapid`, `classical`, `correspondence`, `chess960`, `crazyhouse`, `antichess`, `atomic`, `horde`, `kingOfTheHill`, `racingKings`, `threeCheck`
- for chess.com: `correspondence`, `rapid`, `blitz`, `bullet`

The date ranges can be selected with the flags `--since` and `--until`.
They accept either absolute or relative time ranges:
- absolute: `YYYY`, `YYYY-MM` or `YYYY-MM-DD`
- relative: number with suffix `y` for years, `m` for months, `d` for days or `h` for hours.

All dates specified with `--since` are interpreted as the earliest possible, while `--until` dates are interpreted as the latest possible (see examples)·
All dates are taken in local time.



Examples:
- absolute:
  - `--since 2021`: games since Jan 1 2021
  - `--since 2019 --until 2020`: games between Jan 1 2019 until Dec 31 2020
  - `--since 2018-05-04 --until 2019-07` games between May 4 2018 until July 31 2019
- relative as executed on 2021-06-04 16:30
  - `--since 3m`: games since Mar 1 2021
  - `--since 0d`: games from today
  - `--since 1d`: games since June 3 2021
  - `--until 3m`: games until Mar 31 2021


## Contributing
If you encounter any problems or have suggestions for improvements feel free to open an issue or contact the authors.
