# Main
from logger import logger
from time import sleep

from schedule import every, run_pending
from switchbot import initialize_auth, post_command, get_devices, get_statuses

# Device IDs
plug = "6055F93C4C3A"
bot = "C9864F52A4D7"
# Commands
on = "turnOn"
off = "turnOff"

# Control Record Player
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