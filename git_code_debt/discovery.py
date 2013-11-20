
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt_util.discovery import discover

def is_metric_cls(cls):
    """A metric class is defined as follows:

        - It inherits DiffParserBase
        - It is not DiffParserBase
        - It does not have __metric__ = False
    """
    return (
        cls is not DiffParserBase and
        cls.__dict__.get('__metric__', True) and
        issubclass(cls, DiffParserBase)
    )

def get_metric_parsers(metrics_modules=tuple(), include_defaults=True):
    """Gets all of the metric parsers.

    Args:
        metrics_modules - Defaults to no extra modules, but a metric module
            that contains additional metrics.  A metric inherits DiffParserBase
            and does not have __metric__ = False
            A metric module must be imported using import a.b.c
        include_defaults - Whether to include the generic metric parsers
    """
    metric_parsers = set()

    if include_defaults:
        import git_code_debt.metrics
        metric_parsers.update(discover(git_code_debt.metrics, is_metric_cls))

    for metrics_module in metrics_modules:
        metric_parsers.update(discover(metrics_module, is_metric_cls))
    return metric_parsers

