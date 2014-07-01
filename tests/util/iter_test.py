
import pytest

from git_code_debt_util.iter import chunk_iter


@pytest.mark.parametrize(('input', 'n', 'expected_output'), (
    ([], 1, []),
    ([1, 2], 1, [(1,), (2,)]),
    ([1, 2], 2, [(1, 2)]),
    ([1, 2, 3, 4], 2, [(1, 2), (3, 4)]),
    ([1, 2, 3, 4, 5, 6], 3, [(1, 2, 3), (4, 5, 6)]),
))
def test_chunk_iter(input, n, expected_output):
    output = list(chunk_iter(input, n))
    assert output == expected_output
