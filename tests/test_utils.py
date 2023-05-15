from unittest.mock import MagicMock
import pytest
from pytest_mock import MockerFixture

from app.utils import create_message, send_telegram_msg, CivEvent


@pytest.fixture
def document_mock(mocker: MockerFixture) -> MagicMock:
    get_col_ref_mock = mocker.patch("app.utils.get_collection_ref")
    return get_col_ref_mock.return_value.document.return_value.get.return_value


def test_create_message_no_doc(document_mock: MagicMock) -> None:
    document_mock.exists = False

    civ_event = CivEvent(value1="gameX", value2="playerX", value3="1")
    assert create_message(civ_event) == "@playerX, é o seu turno (1) no game gameX!"


def test_create_message_has_doc(document_mock: MagicMock) -> None:
    document_mock.exists = True
    document_mock.to_dict.return_value = {"telegram_name": "nameX"}

    civ_event = CivEvent(value1="gameX", value2="playerX", value3="1")
    assert create_message(civ_event) == "@nameX, é o seu turno (1) no game gameX!"


def test_send_telegram_msg(mocker: MockerFixture) -> None:
    bot_token = "bot_token"
    chat_id = "chat_id"
    mocker.patch("app.utils.get_secrets", return_value={"bot_token": bot_token, "chat_id": chat_id})
    post_mock: MagicMock = mocker.patch("app.utils.requests.post")

    msg = "msg"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": msg,
    }
    _ = send_telegram_msg(msg)
    post_mock.assert_called_once_with(url, json=data)
