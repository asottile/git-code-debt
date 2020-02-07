import flask


def test_healthcheck(server):
    server.client.get(flask.url_for('status.healthcheck'))
