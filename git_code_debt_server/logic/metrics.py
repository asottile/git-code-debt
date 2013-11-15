

class Metric(object):

    def __init__(self, name, value, sha, date):
        super(Metric, self).__init__()
        self.name = name
        self.value = value
        self.sha = sha
        self.date = date


def metric_names():
    return ['self_dot_display', 'monkey_patch_factory']

def most_recent_metric(metric_name):
    return Metric(metric_name, 50, '', 0)

def metrics_for_dates(repo, sha, metric_name, dates):
    # TODO: WTF is this even doing?
    return [Metric(metric_name, 50, '', date) for date in dates]
