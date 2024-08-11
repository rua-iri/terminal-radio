import logging
import time
import json
import vlc

from helpers import initialise_logs


LOGGING_FILE = f"logs/{time.strftime('%d-%m-%Y')}.log"
LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] - %(message)s"

initialise_logs(LOGGING_FILE)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename=LOGGING_FILE,
    filemode='a',
    format=LOGGING_FORMAT
)


def load_sources() -> list:
    """load radio sources from file

    Raises:
        e: exception (probably because file not found)

    Returns:
        list: a python list of dictionaries
        containing the user's chosen sources
    """
    try:
        with open("src/sources.json") as file:
            src_list = json.load(file)

        return src_list

    except Exception as e:
        raise e


def select_station(src_list: str) -> int:
    try:
        for index, src in enumerate(src_list):
            print(f"{index}: {src.get('name')}")

        station_choice: str = input("\nstation: ")
        station_choice: int = int(station_choice)

        return station_choice

    except ValueError as e:
        raise (e)
        # TODO: handle error if user inputs a string instead
        # of an int (maybe with recursion, but be careful)
    except Exception as e:
        raise e


def play_src(station_src: str):
    try:
        media_player = vlc.MediaPlayer()
        media_src = vlc.Media(station_src)

        media_player.set_media(media_src)
        media_player.play()

        while True:
            pass

    except Exception as e:
        raise e



def main():
    try:
        src_list: list = load_sources()

        print("Choose a station")
        station_choice: int = select_station(src_list=src_list)
        station_src: str = src_list[station_choice].get("url")

        play_src(station_src=station_src)

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    print("\n\n-------------------------")
    main()
