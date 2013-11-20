
import shutil
import testify as T
import tempfile


class TempDirTestCase(T.TestCase):

    @T.setup_teardown
    def create_temp_dir(self):
        self.temp_dir = tempfile.mkdtemp()
        try:
            yield
        finally:
            shutil.rmtree(self.temp_dir)
