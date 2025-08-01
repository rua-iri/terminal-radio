
import json
from pydoc import pager as print_less
import subprocess
import yaml

import inquirer
from inquirer.themes import GreenPassion


def select_station(
        src_list: list,
        message: str = "What Station Would You Like",
        default: str | None = None
) -> dict:
    name_list = [source.get("name") for source in src_list]

    question = inquirer.List('station_name',
                             message=message,
                             choices=name_list,
                             default=default
                             )
    station_name = inquirer.prompt(
        [question],
        theme=GreenPassion(),
        raise_keyboard_interrupt=True
    ).get('station_name')

    for src in src_list:
        if src.get("name") == station_name:
            return src


def clear_screen():
    config = get_config()
    DEBUG = config.get("DEBUG")

    if DEBUG:
        return

    subprocess.run(["clear"])


def get_config():
    with open('resource/config.yaml') as file:
        return yaml.safe_load(file)


def show_stations():
    from .db_dao import DB_DAO
    db_dao = DB_DAO()

    src_list: list = db_dao.get_all_stations()
    print_less(json.dumps(src_list, indent=4))
