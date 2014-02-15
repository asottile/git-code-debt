
import pytest

from testing.assertions.response import assert_no_response_errors
from testing.base_classes.test import test
from testing.utilities.auto_namedtuple import auto_namedtuple


@test
def test_raises_for_response_error():
    with pytest.raises(AssertionError):
        assert_no_response_errors(
            auto_namedtuple(
                response=auto_namedtuple(status_code=201),
            ),
        )

@test
def test_ok_for_200():
    assert_no_response_errors(
        auto_namedtuple(
            response=auto_namedtuple(status_code=200),
        ),
    )
