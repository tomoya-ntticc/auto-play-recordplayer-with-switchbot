# Main
from logger import logger
from time import sleep

import click

from schedule import every, run_pending
from switchbot import initialize_auth, post_command, get_devices, get_status


# Device IDs
plug = "6055F93C4C3A"
bot = "C9864F52A4D7"
# Commands
on = "turnOn"
off = "turnOff"


@click.group()
def cli():
    pass


@cli.command()
def auto_play():
    logger.info("Start auto play record player.")
    get_devices()

    every().minute.at(":30").do(get_status, device_id=plug)

    every().hour.at(":00").do(play)
    every().hour.at(":21").do(stop)
    every().hour.at(":30").do(play)
    every().hour.at(":51").do(stop)

    # Run once a day.
    every().day.at('18:05').do(stop)
    every().day.at('18:10').do(exit)

    while True:
        run_pending()
        sleep(1)


# Control Record Player
@cli.command()
def play():
    initialize_auth()
    logger.info("Play")
    post_command(plug, on)
    sleep(1)
    post_command(bot, on)


@cli.command()
def stop():
    initialize_auth()
    logger.info("Stop")
    post_command(bot, on)
    sleep(4.5)
    post_command(plug, off)


@cli.command()
def status():
    logger.info("Get status")
    get_status(plug)


cli.add_command(auto_play)
cli.add_command(play)
cli.add_command(stop)


if __name__ == "__main__":
    cli()
