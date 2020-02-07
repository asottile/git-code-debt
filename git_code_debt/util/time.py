import calendar
import datetime
from typing import Tuple


def to_timestamp(dt: datetime.datetime) -> int:
    return calendar.timegm(dt.utctimetuple())


def data_points_for_time_range(
        start_timestamp: int,
        end_timestamp: int,
        data_points: int = 25,
) -> Tuple[int, ...]:
    interval = ((end_timestamp - start_timestamp) // data_points) or 1
    return tuple(range(start_timestamp, end_timestamp + interval, interval))
