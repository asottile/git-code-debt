
import argparse
import pkg_resources
import sqlite3

def main():
    parser = argparse.ArgumentParser(description='Set up schema')
    parser.add_argument('database', help='Path to database')
    args = parser.parse_args()

    SQL_FILES = [
        'schema/metric_names.sql',
        'schema/metric_data.sql',
    ]

    with sqlite3.connect(args.database) as db:
        for sql_file in SQL_FILES:
            resource_filename = pkg_resources.resource_filename(
                'git_code_debt', sql_file
            )
            with open(resource_filename, 'r') as resource:
                db.executescript(resource.read())

if __name__ == '__main__':
    main()
