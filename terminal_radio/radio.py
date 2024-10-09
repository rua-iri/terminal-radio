
import logging
import readchar

from classes import Player, Station
from utils import load_sources, select_station, clear_screen


logger = logging.getLogger(__name__)


def monitor_user_input(player: Player, station: Station):
    while True:
        user_char = readchar.readchar()

        if user_char == "q":
            player.stop()
            return

        elif user_char == "r":
            player.restart(url=station.url)

        elif user_char == "\x03":
            raise KeyboardInterrupt


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
        print(station.gen_logo())
        logger.info("Image Rendered")

        print("Now Playing: ", station.name, "\n")
        print("Press 'q' to return to the menu")
        print("Press 'r' to refresh the stream\n")

        logger.info("Playing Radio")

        player.play(url=station.url)

        monitor_user_input(player=player, station=station)

    except KeyboardInterrupt:
        print("\n\nExiting")

        if "player" in vars():
            player.stop()

        clear_screen()
        exit()

    except Exception as e:
        player.stop()
        logger.error(e)


def main():
    while True:
        play_radio()
