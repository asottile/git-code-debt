from __future__ import absolute_import
from __future__ import unicode_literals

import pyquery
import simplejson


class Response(object):
    """A Response wraps a response from a testing Client."""

    def __init__(self, response):
        self.response = response

    @property
    def pq(self):
        return pyquery.PyQuery(self.response.data)

    @property
    def json(self):
        return simplejson.loads(self.response.data)
