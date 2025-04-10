
import subprocess
import inquirer

from inquirer.themes import GreenPassion
import yaml


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
