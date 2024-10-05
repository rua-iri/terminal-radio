
import requests
from urllib.parse import urlparse
from os.path import splitext
from os import remove as delete_file
import inquirer
from inquirer.themes import GreenPassion

from helpers import (load_sources,
                     save_sources,
                     sanitise_string,
                     select_station
                     )


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


def create_source_dev() -> dict:

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

    img_path = save_img(answers.get("img"), answers.get("name"))
    answers.update({"img": img_path})

    return answers


def main():

    options_list: list = [
        "1. Add a new source",
        "2. Remove an existing source"
    ]

    src_list: list = load_sources()

    questions = [inquirer.List(
        "action",
        message="What action would you like to take?",
        choices=[
            options_list[0],
            options_list[1]
        ]
    )]

    user_choice = inquirer.prompt(questions=questions, theme=GreenPassion(),)

    if user_choice.get("action") == options_list[0]:
        new_source: dict = create_source_dev()
        src_list.append(new_source)

    elif user_choice.get("action") == options_list[1]:
        station_choice = select_station(src_list=src_list)

        if station_choice.get("img"):
            delete_file(station_choice.get("img"))

        src_list.remove(station_choice)

    save_sources(src_list)


if __name__ == "__main__":
    main()
