import datetime

def data_points_for_time_range(start_date, end_date, data_points=10):
    interval = (end_date - start_date).days / data_points
    return [start_date + datetime.timedelta(i * interval, 0) for i in range(data_points)]
