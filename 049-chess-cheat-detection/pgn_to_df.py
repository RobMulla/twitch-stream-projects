import pandas as pd
from tqdm.auto import trange
from glob import glob
import os
import chess
import chess.pgn


def pgn_to_df(pgn_file):
    """Pulls metadata from pgn file and puts in dataframe format

    Args:
        pgn_file (str): The file location with pgn games.

    Returns:
        games_df: pandas Dataframe with game details
    """
    headers = []
    games = []
    mainline_moves = []
    with open(pgn_file, mode="r", encoding="utf-8") as pgn:
        while True:
            header = chess.pgn.read_headers(pgn)
            if header is None:
                break
            headers.append(header)

    with open(pgn_file, mode="r", encoding="utf-8") as pgn:
        for _ in trange(len(headers)):
            game = chess.pgn.read_game(pgn)
            games.append(game)
            moves = str(game.mainline_moves())
            mainline_moves.append(moves)
    games_df = pd.DataFrame(headers)
    games_df["mainline_moves"] = mainline_moves
    games_df["Date_clean"] = pd.to_datetime(games_df["Date"], errors="coerce")
    games_df["Online"] = games_df["Site"].str.endswith("INT")
    return games_df


def run(pgn_files):
    for pgn in pgn_files:
        print(f"Running for pgn file {pgn}")
        fn = pgn.split("/")[-1].replace(".pgn", "")
        if os.path.exists(f"games/{fn}.parquet"):
            print("File already exists")
            continue
        try:
            games_df = pgn_to_df(pgn)
            games_df.to_parquet(f"games/{fn}.parquet")
        except Exception as e:
            print(f"Failed for {pgn} with exception {e}")


if __name__ == "__main__":
    pgn_files = glob("pgns/*.pgn")
    run(pgn_files)
