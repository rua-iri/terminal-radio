
import logging
import threading
import readchar

from .classes import LoadingIcon, Player, Station
from .utils import select_station, clear_screen
from .db_dao import DB_DAO

logger = logging.getLogger(__name__)


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
        clear_screen()
        db_dao = DB_DAO()
        loading_icon = LoadingIcon()
        loading_thread = threading.Thread(target=loading_icon.animate)
        player = Player()
        current_station = db_dao.get_last_station()

        src_list: list = db_dao.get_all_stations()

        station_data = select_station(
            src_list=src_list,
            default=current_station
        )

        db_dao.set_last_station(station_data.get("name"))

        loading_thread.start()

        station: Station = Station(**station_data)

        loading_icon.stop()
        loading_thread.join()

        logger.info(f"Station Selected: {station.name}")
        logger.info(f"Station Source: {station.url}")

        station.display_image()

        player.display_options(station.name)
        player.play(url=station.url)
        logger.info("Playing Radio")
        db_dao.close()

        monitor_user_input(player=player, station=station)

    except KeyboardInterrupt:
        if "player" in vars():
            player.stop()

        exit()

    except Exception as e:
        player.stop()
        logger.error(e, exc_info=True)
        loading_icon.stop()


def main():
    while True:
        play_radio()
