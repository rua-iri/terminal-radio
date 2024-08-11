import logging
import time
import json

from helpers import initialise_logs


LOGGING_FILE = f"logs/{time.strftime('%d-%m-%Y')}.log"
LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] - %(message)s"

initialise_logs(LOGGING_FILE)

logger = logging.getLogger(__name__)
logger.warning("\n\n------------------------")
logging.basicConfig(
    level=logging.INFO,
    filename=LOGGING_FILE,
    filemode='a',
    format=LOGGING_FORMAT
)


def load_sources() -> list:
    """load radio sources from file

    Raises:
        e: exception

    Returns:
        list: _description_
    """
    try:
        with open("src/sources.json") as file:
            file_data = json.load(file)

        return file_data

    except Exception as e:
        raise e


def main():
    try:
        pass

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
