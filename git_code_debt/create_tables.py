
import argparse
import pkg_resources
import sqlite3
import sys

from git_code_debt.discovery import get_metric_parsers

SQL_FILES = [
    'schema/metric_names.sql',
    'schema/metric_data.sql',
]

def create_schema(db):
    for sql_file in SQL_FILES:
        resource_filename = pkg_resources.resource_filename(
            'git_code_debt', sql_file
        )
        with open(resource_filename, 'r') as resource:
            db.executescript(resource.read())

def get_metric_ids(metrics_modules, include_defaults):
    metric_ids = []
    metric_parsers = get_metric_parsers(
        metrics_modules=metrics_modules,
        include_defaults=include_defaults,
    )
    for metric_parser_cls in metric_parsers:
        for metric_id in metric_parser_cls().get_possible_metric_ids():
            metric_ids.append(metric_id)
    return set(metric_ids)

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

def populate_metric_ids(db, module_names, skip_defaults):
    modules = get_modules(module_names)
    metric_ids = get_metric_ids(modules, not skip_defaults)

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
    parser.add_argument('modules', type=str, nargs='*', help='Metrics Modules')
    args = parser.parse_args()

    with sqlite3.connect(args.database) as db:
        create_schema(db)
        populate_metric_ids(db, args.modules, args.skip_default_metrics)

if __name__ == '__main__':
    main()
