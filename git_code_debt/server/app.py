from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os.path
import shutil
import sqlite3

import flask
import pkg_resources

from git_code_debt.server.servlets.changes import changes
from git_code_debt.server.servlets.commit import commit
from git_code_debt.server.servlets.graph import graph
from git_code_debt.server.servlets.index import index
from git_code_debt.server.servlets.status import status
from git_code_debt.server.servlets.widget import widget


app = flask.Flask(__name__)
app.register_blueprint(changes)
app.register_blueprint(commit)
app.register_blueprint(graph)
app.register_blueprint(index)
app.register_blueprint(status)
app.register_blueprint(widget)


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
    parser = argparse.ArgumentParser()
    parser.add_argument('database_path', type=str)
    parser.add_argument('-p', '--port', type=int, default=5000)
    parser.add_argument(
        '--debug', action='store_true',
        help=(
            'Run in debug mode (stacktraces + single process). '
            'Not suggested for production.'
        ),
    )
    parser.add_argument(
        '--processes', type=int, default=5,
        help='Number of processes, does not apply to --debug',
    )
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
    kwargs = {
        'port': args.port,
        'debug': args.debug,
    }
    if not args.debug:
        kwargs['processes'] = args.processes

    app.run('0.0.0.0', **kwargs)


if __name__ == '__main__':
    exit(main())
