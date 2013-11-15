
import os.path

from git_code_debt.diff_parser_base import DiffParserBase
from git_code_debt.metrics.base import SimpleLineCounterBase
from git_code_debt_util.discovery import discover

__discovery_paths = set()

METRICS_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'metrics'
)

def register_metrics_folder(path):
    assert os.path.exists(path)
    __discovery_paths.add(path)

# Register our folder
register_metrics_folder(METRICS_FOLDER)

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

