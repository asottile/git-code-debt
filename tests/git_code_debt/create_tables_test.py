
import mock
import os.path
import sqlite3
import sys
import testify as T

from git_code_debt.create_tables import create_schema
from git_code_debt.create_tables import get_metric_ids
from git_code_debt.create_tables import main
from git_code_debt.create_tables import populate_metric_ids
from git_code_debt.discovery import get_metric_parsers_from_args
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

@T.suite('integration')
class TestPopulateMetricIds(TempDirTestCase):

    def test_populate_metric_ids(self):
        db_path = os.path.join(self.temp_dir, 'db.db')

        with sqlite3.connect(db_path) as db:
            create_schema(db)
            populate_metric_ids(db, tuple(), False)

            results = db.execute('SELECT * FROM metric_names')
            # Smoke test assertion
            T.assert_length(
                results,
                len(get_metric_ids(get_metric_parsers_from_args(tuple(), False))),
            )

@T.suite('integration')
class TestCreateTablesIntegration(TempDirTestCase):

    def test_create_tables_smoke(self):
        # Basically make sure it runs without crashing
        db_path = os.path.join(self.temp_dir, 'db.db')
        with mock.patch.object(sys, 'argv', ['', db_path]):
            main()
