
import logging
import readchar

from classes import Player, Station
from utils import load_sources, select_station, clear_screen


logger = logging.getLogger(__name__)


def play_radio():
    try:
        clear_screen()
        player = Player()

        logger.info("Loading Sources...")
        src_list: list = load_sources()
        logger.info("Sources Loaded")

        station_data = select_station(src_list=src_list)
        station: Station = Station(**station_data)

        logger.info(f"Station Selected: {station.name}")
        logger.info(f"Station Source: {station.url}")

        logger.info("Rendering Image...")
        clear_screen()
        print(station.get_logo())
        logger.info("Image Rendered")

        print("Now Playing: ", station.name, "\n")
        print("Press 'q' to return to the menu")

        logger.info("Playing Radio")

        player.play(url=station.url)

        if readchar.readchar() == "q":
            player.stop()

    except KeyboardInterrupt:
        print("\n\nExiting")

        if "player" in vars():
            player.stop()

        exit()

    except Exception as e:
        logger.error(e)


def main():
    while True:
        play_radio()
