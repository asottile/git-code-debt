
from __future__ import print_function

import argparse
import sys

from git_code_debt.discovery import get_metric_parsers_from_args


CYAN = '\033[1;36m'
NORMAL = '\033[0m'


def color(text, color, color_setting):
    if not color_setting:
        return text

    return '{0}{1}{2}'.format(color, text, NORMAL)


def main(argv):
    parser = argparse.ArgumentParser(description='List metric parsers')
    parser.add_argument(
        '--skip-default-metrics',
        default=False,
        action='store_true',
        help='Whether to skip default metrics',
    )
    parser.add_argument(
        '--color',
        default='auto',
        choices=['always', 'never', 'auto'],
    )
    parser.add_argument(
        'metric_package_names',
        type=str,
        nargs='*',
        help='Metric Package Names (such as foo.metrics bar.metrics)',
    )
    args = parser.parse_args(argv)

    color_setting = args.color in ('always', 'auto')

    metric_parsers = get_metric_parsers_from_args(
        args.metric_package_names,
        args.skip_default_metrics,
    )

    metric_parsers_sorted = sorted(
        metric_parsers,
        key=lambda cls: cls.__module__ + cls.__name__
    )

    for metric_parser_cls in metric_parsers_sorted:
        print(
            '{0} {1} {2!r}'.format(
                color(metric_parser_cls.__module__, CYAN, color_setting),
                metric_parser_cls.__name__,
                sorted(metric_parser_cls().get_possible_metric_ids()),
            )
        )


if __name__ == '__main__':
    main(sys.argv[1:])
