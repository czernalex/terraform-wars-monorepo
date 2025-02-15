from http import HTTPStatus


def test_healthcheck(client):
    response = client.get("/healthcheck/")
    assert response.status_code == HTTPStatus.OK
