
import testify as T

from git_code_debt_util.iter import chunk_iter
from testing.base_classes.test import test


INPUTS_TO_EXPECTED_OUTPUTS = (
    ([], 1, []),
    ([1, 2], 1, [(1,), (2,)]),
    ([1, 2], 2, [(1, 2)]),
    ([1, 2, 3, 4], 2, [(1, 2), (3, 4)]),
    ([1, 2, 3, 4, 5, 6], 3, [(1, 2, 3), (4, 5, 6)]),
)

@test
def test_chunk_iter():
    for input, n, expected_output in INPUTS_TO_EXPECTED_OUTPUTS:
        output = list(chunk_iter(input, n))
        T.assert_equal(output, expected_output)
