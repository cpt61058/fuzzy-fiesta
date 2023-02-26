from dbrapper import SQLiteWrapper
from fetcher import ScoresFetcher
from fetcher import Scores
from typing import List
from renderer import SheetsRenderer
import argparse
import sys
import datetime
import config_reader


def prepare_db_connection() -> SQLiteWrapper:
    wrap = SQLiteWrapper()
    wrap.create_connection("../output/data.db")
    create_table = wrap.read_sql_file("../sql/schema.sql")
    wrap.execute_query(create_table)
    return wrap


def fetch_scores(usernames: List[str], scores_url: str) -> List[Scores]:
    scores = []
    fetcher = ScoresFetcher(scores_url)
    for username in usernames:
        score = fetcher.fetch_stats(username)
        if score == None:
            return []
        scores.append(score)
    return scores


def update_saved_scores(wrap: SQLiteWrapper, scores: List[Scores]):
    add_scores = wrap.read_sql_file("../sql/add_scores.sql")

    rows = []
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for score in scores:
        row = [timestamp, score.username, score.easy, score.medium, score.hard]
        rows.append(row)
    wrap.execute_multiparam_query(add_scores, rows)


def read_saved_scores(wrap: SQLiteWrapper):
    select_users = wrap.read_sql_file("../sql/read_scores.sql")
    scores = wrap.execute_read_query(select_users)
    return scores


def print_saved_scores(wrap: SQLiteWrapper):
    scores = read_saved_scores(wrap)
    for score in scores:
        print(score)


def fetch_and_save_scores(wrap: SQLiteWrapper):
    data = config_reader.read_config()
    usernames = config_reader.read_usernames(data)
    scores_url = config_reader.read_stats_url(data)
    scores = fetch_scores(usernames, scores_url)
    if len(scores) == 0:
        return
    update_saved_scores(wrap, scores)


def render_scores(wrap: SQLiteWrapper):
    data = config_reader.read_config()
    usernames = config_reader.read_names(data)
    scores = read_saved_scores(wrap)
    render = SheetsRenderer(config_reader.read_spreadsheet_id(data))
    render.render(scores, usernames)


def config_argparser() -> argparse.ArgumentParser:
    argParser = argparse.ArgumentParser(
        description="Fetches Leetcode for users, stores them in db, and renders in Google Sheets"
    )
    argParser.add_argument(
        "-f", "--fetch", action="store_true", help="Fetch new data and save it in db"
    )
    argParser.add_argument(
        "-r", "--render", action="store_true", help="Render data saved in db"
    )
    argParser.add_argument(
        "-p", "--print", action="store_true", help="Print data saved in db"
    )
    return argParser


def main():
    argParser = config_argparser()
    if len(sys.argv) == 1:
        argParser.print_help(sys.stderr)
        sys.exit(1)
    args = argParser.parse_args()

    wrap = prepare_db_connection()
    if args.fetch:
        fetch_and_save_scores(wrap)
    if args.render:
        render_scores(wrap)
    if args.print:
        print_saved_scores(wrap)


if __name__ == "__main__":
    main()
