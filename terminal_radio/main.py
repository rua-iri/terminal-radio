import logging
import subprocess
import time
import json


LOGGING_FILE = f"logs/{time.strftime('%d-%m-%Y')}.log"
LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] - %(message)s"

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename=LOGGING_FILE,
    filemode='a',
    format=LOGGING_FORMAT
)


def initialise_logs(file_name: str):
    try:
        with open(file_name, "a") as file:
            file.write("\n\n-------------------------\n")
    except Exception as e:
        raise e


def load_sources() -> list:
    """load radio sources from file

    Raises:
        e: exception (probably because file not found)

    Returns:
        list: a python list of dictionaries
        containing the user's chosen sources
    """
    try:
        with open("resource/sources.json") as file:
            src_list = json.load(file)

        return src_list

    except Exception as e:
        raise e


def load_station_logo(img_src: str) -> str:
    try:
        import climage
        img_output = climage.convert(img_src)
        return img_output
    except Exception as e:
        raise e


def select_station(src_list: str) -> int:
    try:
        for index, src in enumerate(src_list):
            print(f"{index + 1}: {src.get('name')}")

        station_choice: str = input("\nStation: ")
        station_choice: int = int(station_choice) - 1

        return station_choice

    except ValueError as e:
        raise (e)
        # TODO: handle error if user inputs a string instead
        # of an int (maybe with recursion, but be careful)
    except Exception as e:
        raise e


def play_src(station_src: str):
    try:
        subprocess.run(
            ['ffplay', station_src, "-nodisp", "-loglevel", "quiet"]
        )
    except Exception as e:
        raise e


def main():
    try:
        src_list: list = load_sources()

        print("Choose a station")
        station_choice: int = select_station(src_list=src_list)
        station_src: str = src_list[station_choice].get("url")
        station_img_src: str = src_list[station_choice].get("img")

        img_output: str = load_station_logo(station_img_src)
        print(f"\n\n{img_output}\n\n")

        play_src(station_src=station_src)

    except KeyboardInterrupt:
        print("Exiting")
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    initialise_logs(LOGGING_FILE)
    main()
