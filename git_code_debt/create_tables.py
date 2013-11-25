
import argparse
import os
import os.path
import pkg_resources
import sqlite3
import sys

from git_code_debt.discovery import get_metric_parsers_from_args

def create_schema(db):
    """Creates the database schema."""
    schema_dir = pkg_resources.resource_filename('git_code_debt', 'schema')
    schema_files = os.listdir(schema_dir)

    for sql_file in schema_files:
        resource_filename = os.path.join(schema_dir, sql_file)
        with open(resource_filename, 'r') as resource:
            db.executescript(resource.read())

def get_metric_ids(metric_parsers):
    metric_ids = set([])
    for metric_parser_cls in metric_parsers:
        for metric_id in metric_parser_cls().get_possible_metric_ids():
            metric_ids.add(metric_id)
    return sorted(metric_ids)

def populate_metric_ids(db, package_names, skip_defaults):
    metric_parsers = get_metric_parsers_from_args(package_names, skip_defaults)
    metric_ids = get_metric_ids(metric_parsers)

    for metric_id in metric_ids:
        db.execute(
            "INSERT INTO metric_names ('name') VALUES (?)", [metric_id]
        )

def main(argv):
    parser = argparse.ArgumentParser(description='Set up schema')
    parser.add_argument('database', help='Path to database')
    parser.add_argument(
        '--skip-default-metrics',
        default=False,
        action='store_true',
        help='Whether to skip default metrics',
    )
    parser.add_argument(
        'metric_package_names',
        type=str,
        nargs='*',
        help='Metric Package Names (such as foo.metrics bar.metrics)',
    )
    args = parser.parse_args(argv)

    with sqlite3.connect(args.database) as db:
        create_schema(db)
        populate_metric_ids(
            db,
            args.metric_package_names,
            args.skip_default_metrics,
        )

if __name__ == '__main__':
    main(sys.argv[1:])
