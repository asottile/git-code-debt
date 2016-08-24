from __future__ import absolute_import
from __future__ import unicode_literals

import json

import pyquery


class Response(object):
    """A Response wraps a response from a testing Client."""

    def __init__(self, response):
        self.response = response

    @property
    def text(self):
        return self.response.data.decode(self.response.charset)

    @property
    def pq(self):
        return pyquery.PyQuery(self.text)

    @property
    def json(self):
        return json.loads(self.text)
