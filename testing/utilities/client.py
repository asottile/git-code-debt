from __future__ import annotations

import json
from typing import TYPE_CHECKING

import flask.testing
import pyquery


class Response:
    """A Response wraps a response from a testing Client."""

    def __init__(self, response):
        self.response = response

    @property
    def text(self):
        return self.response.text

    @property
    def pq(self):
        return pyquery.PyQuery(self.text)

    @property
    def json(self):
        return json.loads(self.text)


if TYPE_CHECKING:
    ClientBase = flask.testing.FlaskClient[Response]
else:
    ClientBase = flask.testing.FlaskClient


class Client(ClientBase):
    """A Client wraps the client given by flask to add other utilities."""

    def open(self, *args, **kwargs):
        return Response(super().open(*args, **kwargs))
