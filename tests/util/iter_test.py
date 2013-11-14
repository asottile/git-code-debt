
import testify as T

from util.iter import chunk_iter

class TestChunkIter(T.TestCase):

    INPUTS_TO_EXPECTED_OUTPUTS = (
        ([], 1, []),
        ([1, 2], 1, [(1,), (2,)]),
        ([1, 2], 2, [(1, 2)]),
        ([1, 2, 3, 4], 2, [(1, 2), (3, 4)]),
        ([1, 2, 3, 4, 5, 6], 3, [(1, 2, 3), (4, 5, 6)]),
    )

    def test_chunk_iter(self):
        for input, n, expected_output in self.INPUTS_TO_EXPECTED_OUTPUTS:
            output = list(chunk_iter(input, n))
            T.assert_equal(output, expected_output)
