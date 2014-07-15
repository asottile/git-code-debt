from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from git_code_debt.util.iter import chunk_iter


@pytest.mark.parametrize(('input_list', 'n', 'expected_output'), (
    ([], 1, []),
    ([1, 2], 1, [(1,), (2,)]),
    ([1, 2], 2, [(1, 2)]),
    ([1, 2, 3, 4], 2, [(1, 2), (3, 4)]),
    ([1, 2, 3, 4, 5, 6], 3, [(1, 2, 3), (4, 5, 6)]),
    ([1, 2], 5, [(1, 2)]),
))
def test_chunk_iter(input_list, n, expected_output):
    output = list(chunk_iter(input_list, n))
    assert output == expected_output
