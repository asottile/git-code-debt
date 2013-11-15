
import os.path

from git_code_debt.diff_parser_base import DiffParserBase
from util.discovery import discover

def is_metric_cls(cls):
    return cls is not DiffParserBase and issubclass(cls, DiffParserBase)

def get_metric_parsers():
    metrics_folder = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'metrics',
    )
    return discover(metrics_folder, is_metric_cls)

