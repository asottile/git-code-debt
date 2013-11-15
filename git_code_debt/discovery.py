
from git_code_debt.diff_parser_base import DiffParserBase
from git_code_debt.metrics.base import SimpleLineCounterBase
import git_code_debt.metrics
from git_code_debt_util.discovery import discover

__discovery_paths = []

def register_metrics_module(path):
    __discovery_paths.append(path)

# Register our metrics
register_metrics_module(git_code_debt.metrics)

METRICS_BASE_CLASSES = [
    DiffParserBase,
    SimpleLineCounterBase,
]

def is_metric_cls(cls):
    return cls not in METRICS_BASE_CLASSES and issubclass(cls, DiffParserBase)

def get_metric_parsers():
    metric_parsers = set()
    for metrics_folder in __discovery_paths:
        metric_parsers.update(discover(metrics_folder, is_metric_cls))
    return metric_parsers

