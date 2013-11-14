import datetime
import flask
import simplejson as json

from git_code_debt_server.render_mako import render_template
from git_code_debt_server.logic import metrics
from util import time

graph = flask.Blueprint('graph', __name__)

@graph.route('/graph/<name>')
def show(name):
    repo = flask.request.args.get('repo')
    ref = flask.request.args.get('ref')
    start_timestamp = int(flask.request.args.get('start'))
    end_timestamp = int(flask.request.args.get('end'))

    start_date = datetime.datetime.fromtimestamp(start_timestamp)
    end_date = datetime.datetime.fromtimestamp(end_timestamp)

    data_points = time.data_points_for_time_range(start_date, end_date)
    metrics_for_dates = metrics.metrics_for_dates(repo, ref, name, data_points)

    return render_template('graph.mako', metrics=json.dumps(metrics_for_dates))
