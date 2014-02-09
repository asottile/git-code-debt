
import datetime
import testify as T

from git_code_debt_util.time import data_points_for_time_range
from git_code_debt_util.time import to_timestamp
from testing.base_classes.test import test


@test
def test_to_timestamp():
    dt = datetime.datetime(2013, 1, 2, 3, 4, 5)
    ret = to_timestamp(dt)
    T.assert_equal(ret, 1357095845)


@test
def test_data_points_for_time_range():
    ret = data_points_for_time_range(1, 25, 5)
    T.assert_equal(
        ret,
        [1, 5, 9, 13, 17, 21, 25],
    )
