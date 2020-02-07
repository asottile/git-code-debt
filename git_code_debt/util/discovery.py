import inspect
import pkgutil
from types import ModuleType
from typing import Any
from typing import Callable
from typing import Set
from typing import Type


def discover(
        package: ModuleType,
        cls_match_func: Callable[[Type[Any]], bool],
) -> Set[Type[Any]]:
    """Returns a set of classes in the directory matched by cls_match_func

    Args:
        path - A Python package
        cls_match_func - Function taking a class and returning true if the
            class is to be included in the output.
    """
    matched_classes = set()

    for _, module_name, _ in pkgutil.walk_packages(
            # https://github.com/python/mypy/issues/1422
            package.__path__,  # type: ignore
            prefix=package.__name__ + '.',
    ):
        module = __import__(module_name, fromlist=['__trash'], level=0)

        # Check all the classes in that module
        for _, imported_class in inspect.getmembers(module, inspect.isclass):
            # Don't include things that are only there due to a side-effect of
            # importing
            if imported_class.__module__ != module.__name__:
                continue

            if cls_match_func(imported_class):
                matched_classes.add(imported_class)

    return matched_classes
