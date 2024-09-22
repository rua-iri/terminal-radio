
import requests

from helpers import load_sources, save_sources, select_station


def save_img(img_url: str) -> str:
    try:
        img_data: requests.Request = requests.get(img_url)

        img_filename: str = "resource/img/" + img_url.split("/")[-1]

        img_file = open(img_filename, "wb")
        img_file.write(img_data.content)

        return img_filename

    except Exception as e:
        raise e


def create_source() -> dict:

    station_name: str = input("What is your station name: ")
    station_url: str = input("What is your station's url: ")

    station_img: str = input("What is your station's logo (the url): ")
    station_img = save_img(station_img)

    station_is_yt: str = input("Is your station a Youtube stream? (y/n): ")
    station_is_yt = "".join(station_is_yt.split()).lower()[0]

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
        station_choice: int = select_station(
            src_list=src_list,
            is_first_call=True
        )

        del src_list[station_choice]

    else:

        print("Invalid choice")

    save_sources(src_list)


if __name__ == "__main__":
    main()
