import flask
import sqlite3
import sys

from git_code_debt_server.servlets.graph import graph
from git_code_debt_server.servlets.index import index

app = flask.Flask(__name__)

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
    database_path = sys.argv[1]
    app.run('0.0.0.0', debug=True)
