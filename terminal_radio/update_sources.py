
import logging
import inquirer
from inquirer.themes import GreenPassion

from .utils import select_station
from .db_dao import DB_DAO


logger = logging.getLogger(__name__)

db_dao = DB_DAO()


def get_user_action(options_list: list) -> str:
    questions: list = [
        inquirer.List(
            "action",
            message="What action would you like to take?",
            choices=[*options_list],
        )
    ]

    user_action = inquirer.prompt(
        questions=questions,
        theme=GreenPassion()
    ).get("action")

    return user_action


def create_source(station_choice: dict = {}) -> dict:
    """Create a new radio source using data submitted by user

    Returns:
        dict: The answers submitted by the user in a dictionary
    """

    questions = [
        inquirer.Text(
            name="name",
            message="What is your station name?",
            default=station_choice.get("name"),
        ),
        inquirer.Text(
            name="url",
            message="What is your station's url?",
            default=station_choice.get("url"),
        ),
        inquirer.Text(
            name="img",
            message="What is your station's logo (the url)?",
            default=station_choice.get("img"),
        ),
        inquirer.Confirm(
            "is_yt",
            message="Is your station a Youtube stream?",
            default=station_choice.get("is_yt"),
        ),
    ]

    answers = inquirer.prompt(questions=questions)

    return answers


def add_new_station() -> None:
    logger.info("Adding new Station")
    new_source: dict = create_source()

    logger.info(f"Station: {new_source}")
    if new_source:
        db_dao.create_station(**new_source)


def remove_station(src_list: list) -> None:
    logger.info("Removing Station")
    station_choice: dict = select_station(src_list=src_list)

    logger.info(f"Station: {station_choice}")
    db_dao.delete_station(station_choice.get('name'))


def edit_station(src_list: list) -> None:
    logger.info("Editing Station")
    station_choice: dict = select_station(src_list=src_list)
    station_id: int = db_dao.get_station_id(station_choice.get('name'))

    logger.info(f"Station: {station_choice}")
    logger.info(f"Index: {station_id}")

    new_source: dict = create_source(station_choice=station_choice)
    logger.info(f"New Station: {station_choice}")

    if new_source:
        db_dao.update_station(station_id, **new_source)


def move_station(src_list: list) -> list:
    station_choice: dict = select_station(src_list=src_list)

    station_position: int = src_list.index(
        select_station(
            src_list=src_list,
            message="Before which Station would you like to place it"
        )
    )

    if station_choice and station_position:
        src_list.remove(station_choice)
        src_list.insert(station_position, station_choice)

    return src_list


def main():
    try:
        logger.info("Updating Sources Started")
        src_list: list = db_dao.select_all_stations()
        logger.info("Source List loaded")

        options_list: list = [
            "1. Add a new source",
            "2. Remove an existing source",
            "3. Edit an existing source",
            "4. Rearrange source list",
        ]

        user_action: str = get_user_action(options_list)

        logger.info(f"User Action: {user_action}")

        if user_action == options_list[0]:
            add_new_station()

        elif user_action == options_list[1]:
            remove_station(src_list=src_list)

        elif user_action == options_list[2]:
            edit_station(src_list=src_list)

        elif user_action == options_list[3]:
            src_list = move_station(src_list=src_list)

    except KeyboardInterrupt:
        print("Cancelled by user")

    except Exception as e:
        logger.error(e)
