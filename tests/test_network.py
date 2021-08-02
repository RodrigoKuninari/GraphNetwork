import http
import pytest


# Probing Test
def test_probe(client, app):
    assert client.get("/").status_code == http.HTTPStatus.OK


# Bad Request Test
def test_bad_request(client, app):
    assert client.get("/network").status_code == http.HTTPStatus.BAD_REQUEST


# Processing Test
@pytest.mark.parametrize("person,expected_result",
[
    # Existing Person
    (
        "Rodrigo",
        ""
    ),
    # Person Not Found
    (
        "Ally",
        "Ally",
    )
])
def test_processing(client, app, person, expected_result):
    result = client.get("/network?name={}".format(person))
    assert result.status_code == http.HTTPStatus.OK
    assert result.json["Person"] == expected_result
