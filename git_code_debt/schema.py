
import argparse
import sqlite3

METRIC_DATA = """CREATE TABLE metric_data (
    repo CHAR(255) NOT NULL,
    sha CHAR(40) NOT NULL,
    metric_id INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    running_value INTEGER NOT NULL,
    PRIMARY KEY (repo, sha, metric_id)
);
"""

METRIC_NAMES = """CREATE TABLE metric_names (
    id INTEGER PRIMARY KEY ASC,
    name CHAR(255) NOT NULL
);
"""

def main():
    parser = argparse.ArgumentParser(description='Set up schema')
    parser.add_argument('database', help='Path to database')
    args = parser.parse_args()

    with sqlite3.connect(args.database) as db:
        db.execute(METRIC_NAMES)
        db.execute(METRIC_DATA)

if __name__ == '__main__':
    main()
