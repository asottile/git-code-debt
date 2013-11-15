import flask
import sqlite3

from git_code_debt_server.config import DATABASE_PATH
from git_code_debt_server.servlets.graph import graph
from git_code_debt_server.servlets.index import index

app = flask.Flask(__name__)

app.register_blueprint(index)
app.register_blueprint(graph)

@app.before_request
def before_request():
    flask.g.db = sqlite3.connect(DATABASE_PATH)

@app.teardown_request
def teardown_request(exception):
    flask.g.db.close()

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
