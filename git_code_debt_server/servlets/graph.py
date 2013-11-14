import datetime
import flask

from util import time

graph = flask.Blueprint('graph', __name__)

@graph.route('/graph/<name>')
def show(name):
    start_timestamp = int(flask.request.args.get('start'))
    end_timestamp = int(flask.request.args.get('end'))

    start_date = datetime.datetime.fromtimestamp(start_timestamp)
    end_date = datetime.datetime.fromtimestamp(end_timestamp)

    return str(time.data_points_for_time_range(start_date, end_date))
