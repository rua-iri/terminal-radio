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
        file = open(file_name, "a")
        file.write("\n\n-------------------------\n")
        file.close()
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


def select_station(src_list: str, is_first_call: bool) -> int:
    try:
        for index, src in enumerate(src_list):
            src_item: str = f"{index + 1}: {src.get('name')}"
            print(src_item) if is_first_call else None

        station_choice: str = input("\nStation: ")
        station_choice_index: int = int(station_choice) - 1

        if station_choice_index > len(src_list) + 1:
            raise ValueError

        return station_choice_index

    except ValueError as e:
        # call this function recursively if the user inputs
        # an invalid datatype e.g. str or out of bounds index
        logger.error(e)
        print("\nError: invalid station number \n")
        return select_station(src_list=src_list, is_first_call=False)
    except Exception as e:
        raise e


def play_src(station_src: str):
    try:
        subprocess.run(
            ['ffplay', station_src, "-nodisp", "-loglevel", "quiet"]
        )
    except Exception as e:
        raise e


def main(terminate_count: int):
    try:
        logger.info("Loading Sources...")
        src_list: list = load_sources()
        logger.info("Sources Loaded")

        print("Choose a station")
        station_choice_index: int = select_station(
            src_list=src_list, is_first_call=True
        )

        terminate_count -= 1

        station: dict = src_list[station_choice_index]
        station_src: str = station.get("url")
        station_img_src: str = station.get("img")

        logger.info(f"Station Selected: {station.get('name')}")
        logger.info(f"Station Source: {station.get('url')}")

        logger.info("Rendering Image...")
        img_output: str = load_station_logo(station_img_src)
        print(f"\n\n{img_output}\n\n")
        logger.info("Image Rendered")

        print(f"Now Playing: {station.get('name')}")
        print("Press Ctrl + c to return to the menu")

        logger.info("Playing Radio")
        play_src(station_src=station_src)

    except KeyboardInterrupt:
        terminate_count += 1
        return terminate_count

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    terminate_count = 1

    initialise_logs(LOGGING_FILE)
    while terminate_count < 3:
        terminate_count = main(terminate_count)

    print("\nExiting")
