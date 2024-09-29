
import requests
from urllib.parse import urlparse
from os.path import splitext
from os import remove as delete_file

from helpers import (load_sources,
                     save_sources,
                     select_station,
                     sanitise_string,
                     display_stations
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


def create_source() -> dict:

    station_name: str = input("What is your station name: ")
    station_url: str = input("What is your station's url: ")

    station_img: str = input("What is your station's logo (the url): ")
    station_img = save_img(station_img, station_name)

    station_is_yt: str = input("Is your station a Youtube stream? (y/n): ")
    station_is_yt = sanitise_string(station_is_yt)[0]

    return {
        "name": station_name,
        "url": station_url,
        "img": station_img,
        "isYT": station_is_yt == "y"
    }


def main():

    src_list: list = load_sources()

    print("Which action would you like to take?")
    print("1. Add a new source")
    print("2. Remove an existing source")

    user_choice: int = int(input("Action: "))

    if user_choice == 1:
        new_source: dict = create_source()
        src_list.append(new_source)

    elif user_choice == 2:
        display_stations(src_list=src_list)
        station_choice: int = select_station(src_list=src_list)

        delete_file(src_list[station_choice].get('img'))

        del src_list[station_choice]

    else:

        print("Invalid choice")

    save_sources(src_list)


if __name__ == "__main__":
    main()
