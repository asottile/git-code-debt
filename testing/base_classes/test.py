
import functools
import testify as T


def test(func):
    """Allows you to make a testify test from a pytest-style function.

    Args:
        func - Argumentless callable
    """
    funcname = (
        'test_{0}'.format(func.__name__)
        if not func.__name__.startswith('test') else func.__name__
    )
    new_func = functools.wraps(func)(lambda self: func())

    cls = type(func.__name__, (T.TestCase,), {funcname: new_func})
    cls.__module__ = func.__module__
    return cls
