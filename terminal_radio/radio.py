
import logging
import readchar

from .classes import Player, PrintC, Station
from .utils import get_config, select_station, clear_screen
from .db_dao import DB_DAO

logger = logging.getLogger(__name__)
config = get_config()


db_dao = DB_DAO()


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
        current_station = db_dao.get_last_station()

        clear_screen()
        player = Player()

        logger.info("Loading Sources...")
        src_list: list = db_dao.select_all_stations()
        logger.info("Sources Loaded")

        station_data = select_station(
            src_list=src_list,
            default=current_station
        )

        current_station_id = db_dao.get_station_id(station_data.get("name"))
        db_dao.set_last_station(current_station_id)
        logger.info(f"Current Station: {current_station}")
        logger.info(f"Current Station id: {current_station_id}")

        station: Station = Station(**station_data)

        logger.info(f"Station Selected: {station.name}")
        logger.info(f"Station Source: {station.url}")

        logger.info("Rendering Image...")
        clear_screen()

        if config.get("USE_SIXEL"):
            station.display_sixel_image()
        else:
            station.display_default_logo()

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
