
import testify as T

def assert_no_response_errors(response):
    # TODO: improve this assertion
    T.assert_equal(response.response.status_code, 200)
