
def assert_no_response_errors(response):
    # TODO: improve this assertion
    assert response.response.status_code == 200
