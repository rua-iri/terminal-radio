
import logging

import sys
import time
from os import makedirs
from os.path import dirname

import update_sources
import radio


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


def main():

    cmd_dict = {
        "play": radio.main,
        "update": update_sources.main
    }

    args = dict(enumerate(sys.argv))
    cmd = args.get(1, "play")

    if cmd in cmd_dict.keys():
        cmd_dict[cmd]()

    else:
        print(f"Error: command '{cmd}' not found")


if __name__ == "__main__":
    initialise_logs(LOGGING_FILE)
    main()
