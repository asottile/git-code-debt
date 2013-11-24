
import argparse
import os
import os.path
import pkg_resources
import sqlite3
import sys

from git_code_debt.discovery import get_metric_parsers

def create_schema(db):
    """Creates the database schema."""
    schema_dir = pkg_resources.resource_filename('git_code_debt', 'schema')
    schema_files = os.listdir(schema_dir)

    for sql_file in schema_files:
        resource_filename = os.path.join(schema_dir, sql_file)
        with open(resource_filename, 'r') as resource:
            db.executescript(resource.read())

def get_metric_ids(metric_packages, include_defaults):
    metric_ids = set([])
    metric_parsers = get_metric_parsers(
        metric_packages=metric_packages,
        include_defaults=include_defaults,
    )
    for metric_parser_cls in metric_parsers:
        for metric_id in metric_parser_cls().get_possible_metric_ids():
            metric_ids.add(metric_id)
    return metric_ids

def get_modules(module_names):
    """Returns module objects for each module name.  Has the side effect of
    importing each module.

    Args:
        module_names - iterable of module names

    Returns:
        Module objects for each module specified in module_names
    """
    modules = []

    for module_name in module_names:
        __import__(module_name)
        modules.append(sys.modules[module_name])

    return modules

def populate_metric_ids(db, package_names, skip_defaults):
    packages = get_modules(package_names)
    metric_ids = get_metric_ids(packages, not skip_defaults)

    for metric_id in metric_ids:
        db.execute(
            "INSERT INTO metric_names ('name') VALUES (?)", [metric_id]
        )

def main():
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
    args = parser.parse_args()

    with sqlite3.connect(args.database) as db:
        create_schema(db)
        populate_metric_ids(
            db,
            args.metric_package_names,
            args.skip_default_metrics,
        )

if __name__ == '__main__':
    main()
