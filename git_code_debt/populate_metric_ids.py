
import argparse
import sqlite3

from git_code_debt_server.logic.metrics import get_metric_ids

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
