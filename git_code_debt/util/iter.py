from __future__ import absolute_import
from __future__ import unicode_literals

import itertools


def chunk_iter(iterable, n):
    """Yields an iterator in chunks

    For example you can do

    for a, b in chunk_iter([1, 2, 3, 4, 5, 6], 2):
        print('{0} {1}'.format(a, b))

    # Prints
    # 1 2
    # 3 4
    # 5 6

    Args:
        iterable - Some iterable
        n - Chunk size (must be greater than 0)
    """
    assert n > 0
    iterable = iter(iterable)

    chunk = tuple(itertools.islice(iterable, n))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(iterable, n))
