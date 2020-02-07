import argparse

from git_code_debt.generate_config import DEFAULT_GENERATE_CONFIG_FILENAME


def add_color(argparser: argparse.ArgumentParser) -> None:
    argparser.add_argument(
        '--color',
        default='auto',
        choices=('always', 'never', 'auto'),
        help='Whether to use color in output.',
    )


def add_generate_config_filename(argparser: argparse.ArgumentParser) -> None:
    argparser.add_argument(
        '-C', '--config-filename', default=DEFAULT_GENERATE_CONFIG_FILENAME,
        help='Path to generate config.',
    )
