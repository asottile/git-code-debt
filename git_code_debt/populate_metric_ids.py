
import argparse
import sqlite3

from git_code_debt.discovery import get_metric_parsers

def get_metric_ids():
    metric_ids = []
    metric_parsers = get_metric_parsers()
    for metric_parser_cls in metric_parsers:
        for metric_id in metric_parser_cls().get_possible_metric_ids():
            metric_ids.append(metric_id)
    return metric_ids

def main():
    parser = argparse.ArgumentParser(description='Sets up metric names')
    parser.add_argument('database', help='Database file')
    args = parser.parse_args()

    with sqlite3.connect(args.database) as database:
        metric_ids = get_metric_ids()

        for metric_id in metric_ids:
            database.execute(
                "INSERT INTO metric_names ('name') VALUES (?)", [metric_id]
            )

if __name__ == '__main__':
    main()
