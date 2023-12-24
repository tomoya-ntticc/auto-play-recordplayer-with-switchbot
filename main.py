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


@click.group(invoke_without_command=True)
@click.option('--auto-stop', is_flag=True)
@click.pass_context
def cli(ctx, auto_stop):
    if ctx.invoked_subcommand:
        ctx.invoked_subcommand
    else:
        auto_play(auto_stop=auto_stop)


@cli.command()
def devices():
    get_devices()


@cli.command()
def status():
    get_status(plug)


@cli.command()
def play():
    play_record_player()


@cli.command()
def stop():
    stop_record_player()


# Control Record Player
def play_record_player():
    initialize_auth()
    logger.info("Play")
    post_command(plug, on)
    sleep(1)
    post_command(bot, on)


def stop_record_player():
    initialize_auth()
    logger.info("Stop")
    post_command(bot, on)
    sleep(4.5)
    post_command(plug, off)


def auto_play(auto_stop: bool):
    logger.info("Start auto play record player.")
    get_devices()

    every().minute.at(":30").do(get_status, device_id=plug)

    every().hour.at(":00").do(play_record_player)
    every().hour.at(":21").do(stop_record_player)
    every().hour.at(":30").do(play_record_player)
    every().hour.at(":51").do(stop_record_player)

    # Run once a day.
    if auto_stop:
        logger.info("Player will be stopping at 18:05.")
        every().day.at('18:05').do(stop_record_player)
        every().day.at('18:10').do(exit)

    while True:
        logger.info("waiting...")
        run_pending()
        sleep(1)


if __name__ == "__main__":
    cli()
