import pytest
from pytest_mock import MockerFixture
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def notify_data() -> dict[str, str]:
    return {"value1": "a", "value2": "b", "value3": "c"}


def test_home(client: TestClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"msg": "Civilization turn notificator."}


def test_notify_ok(mocker: MockerFixture, client: TestClient, notify_data: dict[str, str]) -> None:
    mocker.patch("app.main.create_message")
    send_msg_mock = mocker.patch("app.main.send_telegram_msg")
    send_msg_mock.return_value.status_code = 200

    resp = client.post("/notify/", json=notify_data)
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_notify_create_msg_error(mocker: MockerFixture, client: TestClient, notify_data: dict[str, str]) -> None:
    mocker.patch("app.main.create_message", side_effect=Exception())

    resp = client.post("/notify/", json=notify_data)
    assert resp.status_code == 500
    assert resp.json() == {"detail": "Error while creating the message."}


def test_notify_create_request_error(mocker: MockerFixture, client: TestClient, notify_data: dict[str, str]) -> None:
    mocker.patch("app.main.create_message")
    mocker.patch("app.main.send_telegram_msg", side_effect=Exception())

    resp = client.post("/notify/", json=notify_data)
    assert resp.status_code == 500
    assert resp.json() == {"detail": "Error while creating the request to send the message."}


def test_notify_send_msg_error(mocker: MockerFixture, client: TestClient, notify_data: dict[str, str]) -> None:
    mocker.patch("app.main.create_message")
    send_msg_mock = mocker.patch("app.main.send_telegram_msg")
    send_msg_mock.return_value.status_code = 400

    resp = client.post("/notify/", json=notify_data)
    assert resp.status_code == 500
    assert resp.json() == {"detail": "Error while sending the message."}
