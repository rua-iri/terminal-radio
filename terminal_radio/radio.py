
import logging
import readchar

from .classes import Player, PrintC, Station
from .utils import load_sources, select_station, clear_screen


logger = logging.getLogger(__name__)

current_station = None


def monitor_user_input(player: Player, station: Station):
    while True:
        user_char = readchar.readchar()

        if user_char == "q" or user_char == "Q":
            player.stop()
            return

        elif user_char == "r" or user_char == "R":
            player.restart(url=station.url)

        elif user_char == "\x03":
            raise KeyboardInterrupt


def play_radio():
    try:
        global current_station

        clear_screen()
        player = Player()

        logger.info("Loading Sources...")
        src_list: list = load_sources()
        logger.info("Sources Loaded")

        station_data = select_station(
            src_list=src_list,
            default=current_station
        )

        current_station = station_data.get('name')

        station: Station = Station(**station_data)

        logger.info(f"Station Selected: {station.name}")
        logger.info(f"Station Source: {station.url}")

        logger.info("Rendering Image...")
        clear_screen()
        station.display_sixel_image()

        # TODO run this if the terminal is not capable
        # of displaying a sixel image
        # print(station.gen_logo())

        logger.info("Image Rendered")

        print("\n", "Now Playing: ", station.name, "\n")
        PrintC().error("Press 'q' to return to the menu")
        PrintC().info("Press 'r' to refresh the stream\n")

        logger.info("Playing Radio")

        player.play(url=station.url)

        monitor_user_input(player=player, station=station)

    except KeyboardInterrupt:
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
