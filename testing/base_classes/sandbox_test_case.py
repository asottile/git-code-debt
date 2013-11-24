
import contextlib
import os.path
import sqlite3
import testify as T

from git_code_debt.create_tables import create_schema
from git_code_debt.create_tables import populate_metric_ids
from testing.base_classes.temp_dir_test_case import TempDirTestCase

@T.suite('integration')
class SandboxTestCase(TempDirTestCase):

    @contextlib.contextmanager
    def db(self):
        with sqlite3.connect(self.db_path) as db:
            yield db

    @T.setup
    def setup_sandbox(self):
        self.db_path = os.path.join(self.temp_dir, 'db.db')
        with self.db() as db:
            create_schema(db)
            populate_metric_ids(db, tuple(), False)
