import datetime
import flask

graph = flask.Blueprint('graph', __name__)

@graph.route('/graph/<name>')
def show(name):
    from_timestamp = int(flask.request.args.get('from'))
    to_timestamp = int(flask.request.args.get('to'))

    friendly_from = datetime.datetime.fromtimestamp(from_timestamp)
    friendly_to = datetime.datetime.fromtimestamp(to_timestamp)

    return "Viewing " + name + " from " + str(friendly_from) + " to " + str(friendly_to)
