from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.generate_config import DEFAULT_GENERATE_CONFIG_FILENAME


# TODO: Take the color processing code from pre-commit and package it
def add_color(argparser):
    argparser.add_argument(
        '--color',
        default='auto',
        choices=('always', 'never', 'auto'),
        help='Whether to use color in output.',
    )


def add_generate_config_filename(argparser):
    argparser.add_argument(
        '-C', '--config-filename', default=DEFAULT_GENERATE_CONFIG_FILENAME,
        help='Path to generate config.',
    )
