
import os.path
import sqlite3
import testify as T

from git_code_debt.create_tables import create_schema
from git_code_debt.create_tables import get_modules
from testing.base_classes.temp_dir_test_case import TempDirTestCase

@T.suite('integration')
class TestCreateSchema(TempDirTestCase):

    def test_create_schema(self):
        db_path = os.path.join(self.temp_dir, 'db.db')

        with sqlite3.connect(db_path) as db:
            create_schema(db)

            results = db.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
            table_names = [table_name for table_name, in results]

            T.assert_in('metric_names', table_names)
            T.assert_in('metric_data', table_names)


class TestGetModules(T.TestCase):

    def test_get_modules_no_modules(self):
        ret = get_modules([])
        T.assert_equal(ret, [])

    def test_get_modules_some_modules(self):
        ret = get_modules([
            'git_code_debt.metrics', 'git_code_debt.create_tables',
        ])
        # Not a great assertion, but at least it tests that it works
        T.assert_length(ret, 2)
