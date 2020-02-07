import argparse
from typing import Optional
from typing import Sequence

from git_code_debt import options
from git_code_debt.discovery import get_metric_parsers_from_args
from git_code_debt.generate import get_options_from_config


CYAN = '\033[1;36m'
NORMAL = '\033[0m'


def color(text: str, color_value: str, color_setting: bool) -> str:
    if not color_setting:
        return text
    else:
        return f'{color_value}{text}{NORMAL}'


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description='List metric parsers')
    # optional
    options.add_color(parser)
    options.add_generate_config_filename(parser)
    parsed_args = parser.parse_args(argv)

    color_setting = parsed_args.color in ('always', 'auto')
    args = get_options_from_config(parsed_args.config_filename)

    metric_parsers = get_metric_parsers_from_args(
        args.metric_package_names,
        args.skip_default_metrics,
    )

    metric_parsers_sorted = sorted(
        metric_parsers,
        key=lambda cls: cls.__module__ + cls.__name__,
    )

    for metric_parser_cls in metric_parsers_sorted:
        print(
            '{} {}'.format(
                color(metric_parser_cls.__module__, CYAN, color_setting),
                metric_parser_cls.__name__,
            ),
        )
        for name, description in metric_parser_cls().get_metrics_info():
            description = f': {description}' if description else ''
            print(f'    {name}{description}')
    return 0


if __name__ == '__main__':
    exit(main())
