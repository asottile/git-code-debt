
import fnmatch
import inspect
import os
import os.path
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

def discover(directory, cls_match_func):
    """Returns a set of classes in the directory matched by cls_match_func

    Args:
        directory - Directory to search in relative to the cwd (or absolute)
        cls_match_func - Function taking a class and returning true if the
            class is to be included in the output.
    """
    matched_classes = set()

    # Look for all python files in the jar downloader directory
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if not fnmatch.fnmatch(filename, '*.py'):
                continue

            module_name = get_module_name(root, filename)
            # TODO: testify does something similar and wraps this in a try
            # except.  Is this something I want to do?
            # Import the module
            __import__(module_name)
            module = sys.modules[module_name]

            # Check all the classes in that module
            for name, _ in inspect.getmembers(module, inspect.isclass):
                imported_class = getattr(module, name)

                if cls_match_func(imported_class):
                    matched_classes.add(imported_class)

    return matched_classes
