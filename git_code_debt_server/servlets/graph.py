import datetime
import flask
import simplejson as json

from git_code_debt_server.render_mako import render_template
from git_code_debt_server.logic import metrics
from git_code_debt_util.time import data_points_for_time_range

graph = flask.Blueprint('graph', __name__)

@graph.route('/graph/<name>')
def show(name):
    repo = flask.request.args.get('repo')
    start_timestamp = int(flask.request.args.get('start'))
    end_timestamp = int(flask.request.args.get('end'))

    data_points = data_points_for_time_range(start_timestamp, end_timestamp)
    metrics_for_dates = metrics.metrics_for_dates(repo, name, data_points)

    metrics_for_js = [(m.value, str(datetime.datetime.fromtimestamp(m.date))) for m in metrics_for_dates]

    return render_template('graph.mako', metric_name=name, metrics=json.dumps(metrics_for_js), start_timestamp=start_timestamp, end_timestamp=end_timestamp)
