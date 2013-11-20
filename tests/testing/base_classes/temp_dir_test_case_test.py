
import os.path
import testify as T

from testing.base_classes.temp_dir_test_case import TempDirTestCase

class TestTempDirTestCase(T.TestCase):

    def test_temp_dir_test_case(self):
        instance = TempDirTestCase()

        # Super hacky, but checks the inside of the generator
        for _ in instance.create_temp_dir():
            T.assert_is(os.path.exists(instance.temp_dir), True)

        T.assert_is(os.path.exists(instance.temp_dir), False)
