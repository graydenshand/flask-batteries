from ..fixtures import client, app


def test_index_returns_ok_response(client):
    r = client.get("/")
    assert r.status == "200 OK"
    assert b"Hello World!" in r.data
