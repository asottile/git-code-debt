from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse

from git_code_debt import options
from git_code_debt.discovery import get_metric_parsers_from_args


CYAN = '\033[1;36m'
NORMAL = '\033[0m'


def color(text, color_value, color_setting):
    if not color_setting:
        return text

    return '{0}{1}{2}'.format(color_value, text, NORMAL)


def main(argv=None):
    parser = argparse.ArgumentParser(description='List metric parsers')
    # optional
    options.add_color(parser)
    options.add_skip_default_metrics(parser)
    options.add_metric_package_names(parser)
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
    exit(main())
