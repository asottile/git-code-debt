
from __future__ import absolute_import

import flask

from testing.assertions.response import assert_no_response_errors
from testing.base_classes.git_code_debt_server_test_case import GitCodeDebtServerTestCase

class TestIndex(GitCodeDebtServerTestCase):

    def test_index_loads(self):
        response = self.client.get(flask.url_for('index.show'))
        assert_no_response_errors(response)
