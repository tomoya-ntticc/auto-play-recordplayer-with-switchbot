# SwitchBot
import base64
import hashlib
import hmac
import os
import requests
import uuid
from logger import logger
from pprint import pformat
from time import time

from dotenv import load_dotenv

load_dotenv()

# Endpoint
url = "https://api.switch-bot.com"
# Declare empty header dictionary
apiHeader = {}


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
    logger.info("Get devices")
    res = requests.get(f"{url}/v1.1/devices", headers=apiHeader)
    logger.debug(pformat(res.json()))


def get_status(device_id: str):
    initialize_auth()
    logger.info("Get status")
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