
import subprocess
import inquirer
import json

from inquirer.themes import GreenPassion
import yaml


def load_sources() -> list:
    """Load radio sources from file

    Raises:
        e: exception (probably because file not found)

    Returns:
        list: a python list of dictionaries
        containing the user's chosen sources
    """
    try:
        file = open("resource/sources.json")
        src_list = json.load(file)
        file.close()

        return src_list

    except Exception as e:
        raise e


def save_sources(src_list: list):
    """Save an updated list of sources to the file

    Args:
        src_list (list): _description_

    Raises:
        e: _description_
    """
    try:
        file = open("resource/sources.json", "w")
        json.dump(src_list, file, indent=2)
        file.close()

    except Exception as e:
        raise e


def select_station(
        src_list: list,
        message: str = "What Station Would You Like",
        default: str = None
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
    subprocess.run(["clear"])


def get_config():
    with open('resource/config.yaml') as file:
        return yaml.safe_load(file)
