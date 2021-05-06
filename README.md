# pgn-downloader

`pgn-downloader` is a CLI tool to download chess games from [Lichess](https://lichess.org) or [chess.com](https://chess.com).

It provides filters to specify playing color, date range and playing mode.

## Installation
`pgn-downloader` requires Python >=3.6.

It can then installed with `pip`:
```
pip install git+https://github.com/Simske/pgn-downloader.git
```

With this the tool can started with either:
```
pgn-downloader server username
python -m pgn_downloader server username
```

## Usage
```
usage: pgn-downloader [-h] [--version] [-c {white,black}] [--since SINCE] [--until UNTIL] [--mode MODE] [-o OUTPUT] {chess.com,lichess} username

positional arguments:
  {chess.com,lichess}   Server to download games from
  username              Username on chosen server

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -c {white,black}, --color {white,black}
                        Color (white/black) (default: both)
  --since SINCE         Download games since (default: account creation)
  --until UNTIL         Download games until (default: now)
  --mode MODE           Game mode which will be downloaded. Comma separated list (default: blitz,rapid,classical,correspondence)
  -o OUTPUT, --output OUTPUT
                        Output filename (default: server_username-color.pgn)

```
