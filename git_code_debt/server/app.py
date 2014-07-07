from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import flask
import os.path
import pkg_resources
import shutil
import sqlite3
import sys

from git_code_debt.server.servlets.graph import graph
from git_code_debt.server.servlets.index import index


app = flask.Flask(__name__)
app.register_blueprint(index)
app.register_blueprint(graph)


class AppContext(object):
    database_path = './database.db'


@app.before_request
def before_request():
    # Imported here to avoid stating a non-existent file
    from git_code_debt.server.metric_config_watcher import watcher
    watcher.reload_if_changed()
    flask.g.db = sqlite3.connect(AppContext.database_path)


@app.teardown_request
def teardown_request(_):
    flask.g.db.close()


def create_metric_config_if_not_exists():
    """Creates the sameple metric_config.yaml in the current directory if
    it does not exist.
    """
    if os.path.exists('metric_config.yaml'):
        return

    print('WARNING: no metric_config.yaml detected.  Creating sample config!')
    shutil.copyfile(
        pkg_resources.resource_filename(
            'git_code_debt.server', 'metric_config.sample.yaml',
        ),
        'metric_config.yaml',
    )


def main(argv=None):  # pragma: no cover (starts a web server)
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('database_path', type=str)
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args(argv)

    if not os.path.exists(args.database_path):
        print('Not found: {0}'.format(args.database_path))
        print(
            'Use git-code-debt-create-tables and git-code-debt-generate to '
            'create a database.'
        )
        return 1

    create_metric_config_if_not_exists()

    AppContext.database_path = args.database_path
    app.run('0.0.0.0', port=args.port, debug=True)


if __name__ == '__main__':
    exit(main())
