from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import flask
import sqlite3
import sys

from git_code_debt.server.metric_config import metric_config_watcher
from git_code_debt.server.servlets.graph import graph
from git_code_debt.server.servlets.index import index


app = flask.Flask(__name__)
app.register_blueprint(index)
app.register_blueprint(graph)


class AppContext(object):
    database_path = './database.db'


@app.before_request
def before_request():
    metric_config_watcher.reload_if_changed()
    flask.g.db = sqlite3.connect(AppContext.database_path)


@app.teardown_request
def teardown_request(_):
    flask.g.db.close()


def main(argv=None):  # pragma: no cover (starts a web server)
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('database_path', type=str)
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    # TODO: is there a more elegant way to do this?
    AppContext.database_path = args.database_path
    app.run('0.0.0.0', port=args.port, debug=True)


if __name__ == '__main__':
    exit(main())
