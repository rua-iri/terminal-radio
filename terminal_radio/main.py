
import logging
import signal
import subprocess
import time
from os import get_terminal_size, setsid, killpg, getpgid, makedirs
from os.path import dirname
import readchar

from classes import Station
from helpers import load_sources, select_station


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


def clear_screen():
    subprocess.run(["clear"])


def close_player(process_id: int):
    killpg(
        getpgid(process_id),
        signal.SIGTERM
    )


def display_station_logo(img_src: str):
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
        print(f"\n\n{img_output}\n\n")

    except Exception as e:
        raise e


def play_src(station_src: str) -> subprocess.Popen:
    process = subprocess.Popen(
        f'ffplay {station_src} -nodisp -loglevel quiet -infbuf',
        stdout=subprocess.PIPE,
        shell=True,
        preexec_fn=setsid
    )
    return process


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

        station_data = select_station(src_list=src_list)
        station: Station = Station(**station_data)

        if station.isYT:
            station = fetch_yt_station(station.url)

        logger.info(f"Station Selected: {station.name}")
        logger.info(f"Station Source: {station.url}")

        logger.info("Rendering Image...")

        clear_screen()

        display_station_logo(station.img)
        logger.info("Image Rendered")

        print(f"Now Playing: {station.name}\n")
        print("Press 'q' to return to the menu")

        logger.info("Playing Radio")

        process = play_src(station_src=station.url)

        while True:
            if readchar.readchar() == "q":
                if process:
                    close_player(process.pid)

                return

    except KeyboardInterrupt:
        print("\n\nExiting")

        if "process" in vars():
            close_player(process.pid)

        exit()

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":

    initialise_logs(LOGGING_FILE)
    while True:
        clear_screen()
        main()
