from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import collections
import datetime

import flask

from git_code_debt.server import logic
from git_code_debt.server.presentation.delta import Delta
from git_code_debt.server.render_mako import render_template
from git_code_debt.util.time import to_timestamp


index = flask.Blueprint('index', __name__)

DATE_NAMES_TO_TIMEDELTAS = (
    ('Last Day', datetime.timedelta(days=1)),
    ('Last Week', datetime.timedelta(days=7)),
    ('Last Month', datetime.timedelta(days=30)),
    ('Last 3 Months', datetime.timedelta(days=90)),
    ('Last 6 Months', datetime.timedelta(days=180)),
    ('Last Year', datetime.timedelta(days=365)),
)


Group = collections.namedtuple('Group', ('name', 'metrics'))


class Metric(collections.namedtuple(
        'Metric',
        (
            'name',
            'color_override',
            'current_value',
            'historic_deltas',
            'all_data_url',
        ),
)):
    __slots__ = ()

    @property
    def classname(self):
        if self.color_override:
            return 'color-override'
        else:
            return ''

    @classmethod
    def from_data(
            cls,
            metric_name,
            today_timestamp,
            offsets,
            current_values,
            metric_data,
            color_overrides,
    ):
        return cls(
            metric_name,
            metric_name in color_overrides,
            current_values[metric_name],
            tuple(
                Delta(
                    flask.url_for(
                        'graph.show',
                        metric_name=metric_name,
                        start=str(timestamp),
                        end=str(today_timestamp),
                    ),
                    (
                        current_values[metric_name] -
                        metric_data[time_name][metric_name]
                    ),
                )
                for time_name, timestamp in offsets
            ),
            flask.url_for('graph.all_data', metric_name=metric_name),
        )


def format_groups(
        config,
        metric_names,
        today_timestamp,
        offsets,
        current_values,
        metric_data,
):
    metrics = {
        metric_name: Metric.from_data(
            metric_name,
            today_timestamp,
            offsets,
            current_values,
            metric_data,
            config.color_overrides,
        )
        for metric_name in metric_names
    }

    defined_groups = [
        Group(
            group.name, tuple(
                metrics[metric_name]
                for metric_name in metric_names if group.contains(metric_name)
            ),
        )
        for group in config.groups
    ]

    uncategorized_group = Group(
        'Uncategorized',
        tuple(
            metrics[metric_name]
            for metric_name in metric_names if not any(
                group.contains(metric_name) for group in config.groups
            )
        ),
    )

    all_group = Group(
        'All', tuple(metrics[metric_name] for metric_name in metric_names),
    )

    all_groups = defined_groups + [uncategorized_group, all_group]
    return [group for group in all_groups if group.metrics]


@index.route('/')
def show():
    metric_names = logic.get_metric_ids(flask.g.db)
    today = datetime.datetime.today()
    today_timestamp = to_timestamp(today)
    offsets = [
        (time_name, to_timestamp(today - offset))
        for (time_name, offset) in DATE_NAMES_TO_TIMEDELTAS
    ]
    current_values = logic.get_metrics_for_sha(logic.get_latest_sha())
    metric_data = {
        time_name:
        logic.get_metrics_for_sha(logic.get_sha_for_date(timestamp))
        for (time_name, timestamp) in offsets
    }

    return render_template(
        'index.mako',
        groups=format_groups(
            flask.g.config,
            metric_names,
            today_timestamp,
            offsets,
            current_values,
            metric_data,
        ),
    )
