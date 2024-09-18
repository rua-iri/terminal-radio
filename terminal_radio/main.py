import logging
import subprocess
import time
import json
from os import get_terminal_size
from ffpyplayer.player import MediaPlayer

from classes import Station


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


def clear_screen():
    subprocess.run(["clear"])


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

        terminal_cols, terminal_lines = get_terminal_size()
        img_width: int = int(terminal_cols / 2)

        import climage
        img_output = climage.convert(
            filename=img_src,
            is_unicode=True,
            is_256color=True,
            width=img_width
        )
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


def play_src(station_src: str) -> MediaPlayer:
    player: MediaPlayer = MediaPlayer(station_src)
    return player


def fetch_yt_station(url: str) -> Station:
    import yt_dlp
    import requests

    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)

    img_url: str = info.get("thumbnail")
    res: requests.Response = requests.get(img_url)
    img_filename: str = "resource/img/yt_img.jpg"

    with open(img_filename, 'wb') as img_file:
        img_file.write(res.content)

    yt_station = Station(
        name=info.get("fulltitle"),
        url=info.get("url"),
        img=img_filename,
        isYT=True
    )

    return yt_station


def main():
    try:
        logger.info("Loading Sources...")
        src_list: list = load_sources()
        logger.info("Sources Loaded")

        print("Choose a station")
        station_index: int = select_station(
            src_list=src_list, is_first_call=True
        )

        if src_list[station_index].get("isYT"):
            station: Station = fetch_yt_station(
                src_list[station_index].get("url"))
        else:
            station: Station = Station(**src_list[station_index])

        logger.info(f"Station Selected: {station.name}")
        logger.info(f"Station Source: {station.url}")

        logger.info("Rendering Image...")

        clear_screen()

        img_output: str = load_station_logo(station.img)
        print(f"\n\n{img_output}\n\n")
        logger.info("Image Rendered")

        print(f"Now Playing: {station.name}\n")
        print("Send letter 'q' to return to the menu")

        logger.info("Playing Radio")

        player: MediaPlayer = play_src(station_src=station.url)

        while True:
            if input("Letter: ") == "q":
                player.close_player()
                return

    except KeyboardInterrupt:
        print("\n\nExiting")
        exit()

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":

    initialise_logs(LOGGING_FILE)
    while True:
        clear_screen()
        main()
