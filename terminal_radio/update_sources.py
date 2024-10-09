
import json
import requests
from urllib.parse import urlparse
from os.path import splitext, isfile
from os import remove as delete_file
import inquirer
from inquirer.themes import GreenPassion

from utils import (load_sources,
                   save_sources,
                   sanitise_string,
                   select_station
                   )


def get_user_action(options_list: list) -> str:

    questions: list = [inquirer.List(
        "action",
        message="What action would you like to take?",
        choices=[
            *options_list
        ]
    )]

    user_action = inquirer.prompt(
        questions=questions,
        theme=GreenPassion()
    ).get("action")

    return user_action


def save_img(img_url: str, station_name: str) -> str:
    """Save a station's logo to file

    Args:
        img_url (str): The URL of the image

    Raises:
        e: Generic Error

    Returns:
        str: The filename of the new image
    """
    try:
        if isfile(img_url):
            return img_url

        img_data: requests.Request = requests.get(img_url)

        url_path = urlparse(img_url).path
        img_filename = "resource/img/"
        img_filename += sanitise_string(station_name)
        img_filename += splitext(url_path)[1]

        img_file = open(img_filename, "wb")
        img_file.write(img_data.content)

        return img_filename

    except Exception as e:
        raise e


def create_source() -> dict:
    """Create a new radio source using data submitted by user

    Returns:
        dict: The answers submitted by the user in a dictionary
    """

    questions = [
        inquirer.Text(name='name',
                      message="What is your station name?"),
        inquirer.Text(name='url',
                      message="What is your station's url?"),
        inquirer.Text(name='img',
                      message="What is your station's logo (the url)?"),
        inquirer.Confirm('isYT',
                         message="Is your station a Youtube stream?")
    ]

    answers = inquirer.prompt(questions=questions)

    img_path = save_img(
        img_url=answers.get("img"),
        station_name=answers.get("name")
    )
    answers.update({"img": img_path})

    return answers


def edit_source(station_choice: dict) -> dict:
    """Edit the source data for a station

    Args:
        station_choice (dict): A dictionary of the station that
        the user wishes to edit

    Returns:
        dict: The answers submitted by the user in a dictionary
    """
    questions = [
        inquirer.Text(name='name',
                      message="What is your station name?",
                      default=station_choice.get("name")),
        inquirer.Text(name='url',
                      message="What is your station's url?",
                      default=station_choice.get("url")),
        inquirer.Text(name='img',
                      message="What is your station's logo (the url)?",
                      default=station_choice.get("img")),
        inquirer.Confirm('isYT',
                         message="Is your station a Youtube stream?",
                         default=station_choice.get("isYT"))
    ]

    answers = inquirer.prompt(questions=questions)

    img_path = save_img(
        img_url=answers.get("img"),
        station_name=answers.get("name")
    )
    answers.update({"img": img_path})

    return answers


def add_new_station(src_list: list) -> list:
    new_source: dict = create_source()
    src_list.append(new_source)
    return src_list


def remove_station(src_list: list) -> list:
    station_choice: dict = select_station(src_list=src_list)

    if station_choice.get("img"):
        delete_file(station_choice.get("img"))

    src_list.remove(station_choice)

    return src_list


def edit_station(src_list: list) -> list:
    station_choice: dict = select_station(src_list=src_list)
    src_list.remove(station_choice)

    new_source: dict = edit_source(
        station_choice=station_choice
    )
    src_list.append(new_source)

    return src_list


def move_station(src_list: list) -> list:
    station_choice: dict = select_station(src_list=src_list)

    station_position: int = src_list.index(
        select_station(
            src_list=src_list,
            message="Before which Station would you like to place it"
        )
    )

    src_list.remove(station_choice)
    src_list.insert(station_position, station_choice)

    return src_list


def main():
    src_list: list = load_sources()

    options_list: list = [
        "1. Add a new source",
        "2. Remove an existing source",
        "3. Edit an existing source",
        "4. Rearrange source list",
        "5. View Sources"
    ]

    user_action = get_user_action(options_list)

    if user_action == options_list[0]:
        src_list = add_new_station(src_list=src_list)

    elif user_action == options_list[1]:
        src_list = remove_station(src_list=src_list)

    elif user_action == options_list[2]:
        src_list = edit_station(src_list=src_list)

    elif user_action == options_list[3]:
        src_list = move_station(src_list=src_list)

    elif user_action == options_list[4]:
        print(json.dumps(src_list, indent=4))

    save_sources(src_list)


if __name__ == "__main__":
    main()
