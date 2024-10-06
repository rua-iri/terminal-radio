
import signal
import subprocess
from os import get_terminal_size, setsid, killpg, getpgid
import logging
import readchar

from classes import Station
from utils import load_sources, select_station, clear_screen


logger = logging.getLogger(__name__)


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

    logger.info("Fetching Youtube Data")

    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)

    img_url: str = info.get("thumbnail")
    res: requests.Response = requests.get(img_url)
    img_filename: str = "resource/img/yt_img.jpg"

    with open(img_filename, 'wb') as img_file:
        img_file.write(res.content)

    logger.info("Youtube Data: ", info)

    logger.info("Station Title: ", info.get('fulltitle'))
    logger.info("Station URL: ", info.get('url'))

    yt_station = Station(
        name=info.get("fulltitle"),
        url=info.get("url"),
        img=img_filename,
        isYT=True
    )

    if not yt_station.url:
        logger.error("No Youtube Stream Found")
        raise Exception("Youtube Stream Not Found")

    return yt_station


def play_radio():
    try:
        clear_screen()
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


def main():
    while True:
        play_radio()
