
import inspect
import os
import os.path
import pkgutil
import sys

def get_module_name(root, filename):
    """Returns the module name for a python file.

    Args:
        root - Path to file's directory
        filename - Name of the python file.
    """
    if not filename.endswith('.py'):
        raise ValueError('filename must end with .py')

    filename = filename[:-3]
    joined_path = os.path.join(root, filename)
    relpath = os.path.relpath(
        joined_path,
        os.path.join(os.path.dirname(__file__), '../'),
    )
    # XXX: should really use pathsep here
    return relpath.replace('/', '.')

def discover(package, cls_match_func):
    """Returns a set of classes in the directory matched by cls_match_func

    Args:
        path - A Python package
        cls_match_func - Function taking a class and returning true if the
            class is to be included in the output.
    """
    matched_classes = set()

    for importer, module_name, ispkg in pkgutil.walk_packages(
        package.__path__,
        prefix=package.__name__ + '.',
    ):
        __import__(module_name)
        module = sys.modules[module_name]

        # Check all the classes in that module
        for name, _ in inspect.getmembers(module, inspect.isclass):
            imported_class = getattr(module, name)

            if cls_match_func(imported_class):
                matched_classes.add(imported_class)

    return matched_classes
