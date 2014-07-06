from __future__ import absolute_import
from __future__ import unicode_literals

import os.path
import sqlite3

from git_code_debt.create_tables import create_schema
from git_code_debt.create_tables import get_metric_ids
from git_code_debt.create_tables import main
from git_code_debt.create_tables import populate_metric_ids
from git_code_debt.discovery import get_metric_parsers_from_args


def test_create_schema(tmpdir):
    db_path = os.path.join(tmpdir.strpath, 'db.db')

    with sqlite3.connect(db_path) as db:
        create_schema(db)

        results = db.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
        table_names = [table_name for table_name, in results]

        assert 'metric_names' in table_names
        assert 'metric_data' in table_names


def test_populate_metric_ids(tmpdir):
    db_path = os.path.join(tmpdir.strpath, 'db.db')

    with sqlite3.connect(db_path) as db:
        create_schema(db)
        populate_metric_ids(db, tuple(), False)

        results = db.execute('SELECT * FROM metric_names').fetchall()
        # Smoke test assertion
        assert (
            len(results) ==
            len(get_metric_ids(get_metric_parsers_from_args(tuple(), False)))
        )


def test_create_tables_smoke(tmpdir):
    # Basically make sure it runs without crashing
    db_path = os.path.join(tmpdir.strpath, 'db.db')
    main([db_path])
