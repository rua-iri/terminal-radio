
import logging
import inquirer
from inquirer.themes import GreenPassion
import prompt_toolkit

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

    answers = {
        "name": prompt_toolkit.prompt(
            message="What is your station name? : ",
            default=station_choice.get("name") or '',
        ),
        "url": prompt_toolkit.prompt(
            message="What is your station's url? : ",
            default=station_choice.get("url") or '',
        ),
        "img": prompt_toolkit.prompt(
            message="What is your station's logo (the url)? : ",
            default=station_choice.get("img") or '',
        ),
        "is_yt": prompt_toolkit.shortcuts.yes_no_dialog(
            title='Youtube Stream',
            text='Is your source a Youtube Stream?'
        ).run()
    }

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


def main():
    try:
        logger.info("Updating Sources Started")
        src_list: list = db_dao.select_all_stations()
        logger.info("Source List loaded")

        options_list: list = [
            "1. Add a new source",
            "2. Remove an existing source",
            "3. Edit an existing source",
        ]

        user_action: str = get_user_action(options_list)

        logger.info(f"User Action: {user_action}")

        if user_action == options_list[0]:
            add_new_station()

        elif user_action == options_list[1]:
            remove_station(src_list=src_list)

        elif user_action == options_list[2]:
            edit_station(src_list=src_list)

    except KeyboardInterrupt:
        print("Cancelled by user")

    except Exception as e:
        logger.error(e)

    finally:
        db_dao.close()
