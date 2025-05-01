
import logging

import sys
import time
from os import makedirs
from os.path import dirname

from terminal_radio import statistics, update_sources
from terminal_radio import radio
from terminal_radio.classes import PrintC
from terminal_radio.utils import show_stations


LOGGING_FILE = f"logs/{time.strftime('%Y/%m')}/{time.strftime('%d-%m-%Y')}.log"
LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] - %(message)s"

makedirs(
    dirname(LOGGING_FILE),
    exist_ok=True
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename=LOGGING_FILE,
    filemode='a',
    format=LOGGING_FORMAT
)


def initialise_logs(file_name: str):
    try:
        file = open(file_name, "a")
        file.write("\n\n-------------------------\n")
        file.close()
    except Exception as e:
        raise e


def show_logs():
    logger.info("Printing logs")
    try:
        file = open(LOGGING_FILE)
        print(file.read())
        file.close()
    except Exception as e:
        raise e


def show_help():
    help_statement: str = """
play - Run the application to listen to radio stations
update - Update the list of available stations
logs - View the application's logs to debug issues
show - Show a JSON formatted list of the currently available stations
stats - Show the top 5 stations by play count
help - Display this help menu
"""

    print(help_statement)


def main():
    initialise_logs(LOGGING_FILE)

    cmd_dict = {
        "play": radio.main,
        "update": update_sources.main,
        "logs": show_logs,
        "show": show_stations,
        "stats": statistics.main,
        "help": show_help
    }

    args = dict(enumerate(sys.argv))
    user_cmd = args.get(1, "play")

    if user_cmd in cmd_dict.keys():
        cmd_dict[user_cmd]()

    else:
        print(f"Error: command '{user_cmd}' not found\n")
        print("Run the following to view a list of available command\n")
        PrintC().info("terminal_radio help")


if __name__ == "__main__":
    main()
