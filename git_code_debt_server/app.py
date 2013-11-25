import argparse
import flask
import sqlite3

from git_code_debt_server.servlets.graph import graph
from git_code_debt_server.servlets.index import index

app = flask.Flask('git_code_debt_server')

app.register_blueprint(index)
app.register_blueprint(graph)

database_path = './database.db'

@app.before_request
def before_request():
    flask.g.db = sqlite3.connect(database_path)

@app.teardown_request
def teardown_request(exception):
    flask.g.db.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('database_path', type=str)
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    database_path = args.database_path
    app.run('0.0.0.0', port=args.port, debug=True)
