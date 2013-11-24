
import os.path
import testify as T

from testing.base_classes.sandbox_test_case import SandboxTestCase

class SandboxSmokeTest(SandboxTestCase):

    def test_db_path_exists(self):
        T.assert_is(os.path.exists(self.db_path), True)

    def test_tables_exists(self):
        with self.db() as db:
            results = db.execute(
                "SELECT * FROM sqlite_master WHERE type='table'"
            ).fetchall()
            T.assert_gt(len(results), 0)
