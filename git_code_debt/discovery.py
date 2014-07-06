from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.util.discovery import discover


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


def get_metric_parsers(metric_packages=tuple(), include_defaults=True):
    """Gets all of the metric parsers.

    Args:
        metric_packages - Defaults to no extra packages. An iterable of
            metric containing packages.  A metric inherits DiffParserBase
            and does not have __metric__ = False
            A metric package must be imported using import a.b.c
        include_defaults - Whether to include the generic metric parsers
    """
    metric_parsers = set()

    if include_defaults:
        import git_code_debt.metrics
        metric_parsers.update(discover(git_code_debt.metrics, is_metric_cls))

    for metric_package in metric_packages:
        metric_parsers.update(discover(metric_package, is_metric_cls))
    return metric_parsers


def get_modules(module_names):
    """Returns module objects for each module name.  Has the side effect of
    importing each module.

    Args:
        module_names - iterable of module names

    Returns:
        Module objects for each module specified in module_names
    """
    return [
        __import__(module_name, fromlist=[str('__trash__')])
        for module_name in module_names
    ]


def get_metric_parsers_from_args(metric_package_names, skip_defaults):
    packages = get_modules(metric_package_names)
    return get_metric_parsers(
        metric_packages=packages, include_defaults=not skip_defaults,
    )
