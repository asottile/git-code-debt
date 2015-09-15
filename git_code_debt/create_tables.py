from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import os
import os.path
import sqlite3

import pkg_resources

from git_code_debt import options
from git_code_debt import write_logic
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
    write_logic.insert_metric_ids(db, metric_ids)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Set up schema')
    # optional
    options.add_skip_default_metrics(parser)
    # positional
    options.add_database(parser)
    options.add_metric_package_names(parser)
    args = parser.parse_args(argv)

    with sqlite3.connect(args.database) as db:
        create_schema(db)
        populate_metric_ids(
            db,
            args.metric_package_names,
            args.skip_default_metrics,
        )


if __name__ == '__main__':
    exit(main())
