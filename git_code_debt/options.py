from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.util import five


# TODO: Take the color processing code from pre-commit and package it
def add_color(argparser):
    argparser.add_argument(
        '--color',
        default='auto',
        choices=('always', 'never', 'auto'),
        help='Whether to use color in output.',
    )


def add_database(argparser):
    argparser.add_argument(
        'database',
        help='Database filename (usually end with .db).'
    )


def add_metric_package_names(argparser):
    argparser.add_argument(
        'metric_package_names',
        type=five.text,
        nargs='*',
        help='Metric Package Names (such as foo.metrics bar.metrics).',
    )


def add_repo(argparser):
    argparser.add_argument(
        'repo',
        help='Git url to a repository to generate metrics from.',
    )


def add_skip_default_metrics(argparser):
    argparser.add_argument(
        '--skip-default-metrics',
        default=False,
        action='store_true',
        help='Whether to skip default metrics.',
    )


def add_tempdir_location(argparser):
    argparser.add_argument(
        '--tempdir-location',
        type=five.text,
        default=None,
        help='Override location of temp dirs.  Default is system default.',
    )
