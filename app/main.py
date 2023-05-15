import logging
import traceback
from fastapi import FastAPI, HTTPException
import uvicorn

from app.utils import create_message, send_telegram_msg, CivEvent

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)
app = FastAPI()


@app.get("/")
def home() -> dict[str, str]:
    return {"msg": "Civilization turn notificator."}


@app.post("/notify/")
def nofity(civ_event: CivEvent) -> dict[str, str]:
    logging.info(
        f"Event received: game_name -> {civ_event.value1} | player_name -> {civ_event.value2} | "
        f"turn_number -> {civ_event.value3}"
    )

    try:
        msg = create_message(civ_event)
    except Exception:
        error_msg = "Error while creating the message."
        logging.error(error_msg)
        logging.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

    try:
        resp = send_telegram_msg(msg)
    except Exception:
        error_msg = "Error while creating the request to send the message."
        logging.error(error_msg)
        logging.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

    if resp.status_code != 200:
        error_msg = "Error while sending the message."
        logging.error(error_msg)
        logging.debug(f"Code: {resp.status_code} - Msg: {resp.json()['description']}.")
        raise HTTPException(status_code=500, detail=error_msg)

    return {"status": "ok"}


def main() -> None:
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    main()
