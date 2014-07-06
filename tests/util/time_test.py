from __future__ import absolute_import
from __future__ import unicode_literals

import datetime

from git_code_debt.util.time import data_points_for_time_range
from git_code_debt.util.time import to_timestamp


def test_to_timestamp():
    dt = datetime.datetime(2013, 1, 2, 3, 4, 5)
    ret = to_timestamp(dt)
    assert ret == 1357095845


def test_data_points_for_time_range():
    ret = data_points_for_time_range(1, 25, 5)
    assert ret == [1, 5, 9, 13, 17, 21, 25]


def test_data_points_for_time_range_gives_data_for_empty_range():
    ret = data_points_for_time_range(1, 1, 5)
    assert ret == [1]
