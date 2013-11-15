
def data_points_for_time_range(start_timestamp, end_timestamp, data_points=25):
    interval = (end_timestamp - start_timestamp) / data_points
    return range(start_timestamp, end_timestamp + interval, interval)
