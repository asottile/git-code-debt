import calendar
import datetime
import flask

from git_code_debt_server.render_mako import render_template
from git_code_debt_server.logic import metrics

index = flask.Blueprint('index', __name__)

@index.route('/')
def show():
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(180)

    start_timestamp = calendar.timegm(start_date.utctimetuple())
    end_timestamp = calendar.timegm(end_date.utctimetuple())

    most_recent_metrics = [metrics.most_recent_metric(m) for m in metrics.metric_names()]

    return render_template('index.mako', metrics=[
        {
            'title': m.name,
            'occurrences': m.value,
            'change': 0,
            'href': flask.url_for('graph.show', name=m.name, sha=m.sha, start=str(start_timestamp), end=str(end_timestamp))
        }
        for m in most_recent_metrics
    ])
