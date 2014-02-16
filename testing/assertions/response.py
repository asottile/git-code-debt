
import urlparse


def assert_no_response_errors(response):
    # TODO: improve this assertion
    assert response.response.status_code == 200


def assert_redirect(response, path, query, redirect_status_code=302):
    assert response.response.status_code == redirect_status_code
    parsed_redirect = urlparse.urlparse(response.response.location)
    assert parsed_redirect.path == path
    parsed_query_string = urlparse.parse_qs(parsed_redirect.query)
    assert parsed_query_string == query
