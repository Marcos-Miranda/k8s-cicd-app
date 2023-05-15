import requests
from pydantic import BaseModel
from google.cloud.firestore import Client, CollectionReference
from google.cloud.secretmanager import SecretManagerServiceClient

collection_ref = None
bot_token = None
chat_id = None


class CivEvent(BaseModel):
    """Data that Civilization sends on a turn event."""

    value1: str  # game name
    value2: str  # player name
    value3: str  # turn number


def get_collection_ref() -> CollectionReference:
    """Get the collection reference of users, initializing the firestore client if needed."""

    global collection_ref
    if collection_ref is None:
        db_client = Client()
        collection_ref = db_client.collection("users")
    return collection_ref


def create_message(civ_event: CivEvent) -> str:
    """Create the message that will be sent to Telegram."""

    document = get_collection_ref().document(civ_event.value2).get()
    if document.exists:
        tele_name = document.to_dict()["telegram_name"]
    else:
        tele_name = civ_event.value2
    return f"@{tele_name}, é o seu turno ({civ_event.value3}) no game {civ_event.value1}!"


def get_secrets() -> dict[str, str]:
    """Get the bot_token and chat_id secrets, initializing the secret manager client if needed."""

    global bot_token, chat_id
    if not (bot_token and chat_id):
        client = SecretManagerServiceClient()
        bot_token = client.access_secret_version(
            name="projects/284185285723/secrets/telegram_bot_token/versions/1"
        ).payload.data.decode("UTF-8")
        chat_id = client.access_secret_version(
            name="projects/284185285723/secrets/telegram_chat_id/versions/1"
        ).payload.data.decode("UTF-8")
    return {"bot_token": bot_token, "chat_id": chat_id}


def send_telegram_msg(msg: str) -> requests.Response:
    """Send the message to the Telegram chat."""

    secrets = get_secrets()
    url = f"https://api.telegram.org/bot{secrets['bot_token']}/sendMessage"
    data = {
        "chat_id": secrets["chat_id"],
        "text": msg,
    }
    return requests.post(url, json=data)
