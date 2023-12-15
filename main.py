# SwitchBot
import base64
import hashlib
import hmac
import os
import requests
import uuid
from logger import logger
from pprint import pformat
from time import sleep, time

from dotenv import load_dotenv
from schedule import every, run_pending

load_dotenv()

# Endpoint
url = "https://api.switch-bot.com"
# Declare empty header dictionary
apiHeader = {}

# Device IDs
plug = "6055F93C4C3A"
bot = "C9864F52A4D7"
# Commands
on = "turnOn"
off = "turnOff"

def initialize_auth():
    token = os.getenv("TOKEN")
    secret = os.getenv("SECRET")
    nonce = uuid.uuid4()
    t = int(round(time() * 1000))
    sign = base64.b64encode(
        hmac.new(
            bytes(secret, "utf-8"),
            msg=bytes("{}{}{}".format(token, t, nonce), "utf-8"),
            digestmod=hashlib.sha256).digest()
    )

    #Build api header JSON
    apiHeader["Authorization"]=token
    apiHeader["Content-Type"]="application/json"
    apiHeader["charset"]="utf8"
    apiHeader["t"]=str(t)
    apiHeader["sign"]=str(sign, "utf-8")
    apiHeader["nonce"]=str(nonce)
    logger.debug(pformat(apiHeader))


def get_devices():
    initialize_auth()
    res = requests.get(f"{url}/v1.1/devices", headers=apiHeader)
    logger.debug(pformat(res.json()))


def get_statuses(device_id: str):
    initialize_auth()
    res = requests.get(f"{url}/v1.1/devices/{device_id}/status", headers=apiHeader)
    logger.debug(pformat(res.json()))


def post_command(device_id: str, command: str):
    request_body = {
        "command": command,
        "parameter": "default",
        "commandType": "command"
    }
    res = requests.post(f"{url}/v1.1/devices/{device_id}/commands", headers=apiHeader, json=request_body)
    logger.debug(pformat(res.json()))


def play():
    initialize_auth()
    post_command(plug, on)
    sleep(1)
    post_command(bot, on)
    logger.info("Play.")


def stop():
    initialize_auth()
    post_command(bot, on)
    sleep(4)
    post_command(plug, off)
    logger.info("Stop.")


# Main
logger.info("Start auto play record player.")
get_devices()

every().minute.at(":30").do(get_statuses, device_id=plug)

every().hour.at(":00").do(play)
every().hour.at(":21").do(stop)
every().hour.at(":30").do(play)
every().hour.at(":51").do(stop)

# Run once a day.
# every().day.at('18:05').do(stop)

while True:
    run_pending()
    sleep(1)