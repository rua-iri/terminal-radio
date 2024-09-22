

import json


def load_sources() -> list:
    """load radio sources from file

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
    try:
        file = open("resource/sources.json", "w")
        json.dump(src_list, file)
        file.close()

    except Exception as e:
        raise e


def select_station(src_list: str, is_first_call: bool) -> int:
    """Select a station from the list of stations

    Args:
        src_list (str): A list of the stations
        is_first_call (bool): Is first time that function is being called

    Raises:
        ValueError: Error if index is outside the list range
        e: Generic Error

    Returns:
        int: _description_
    """
    try:
        for index, src in enumerate(src_list):
            src_item: str = f"{index + 1}: {src.get('name')}"
            print(src_item) if is_first_call else None

        station_choice: str = input("\nStation: ")
        station_choice_index: int = int(station_choice) - 1

        if station_choice_index > len(src_list) + 1:
            raise ValueError

        return station_choice_index

    except ValueError:
        # call this function recursively if the user inputs
        # an invalid datatype e.g. str or out of bounds index
        print("\nError: invalid station number \n")
        return select_station(src_list=src_list, is_first_call=False)
    except Exception as e:
        raise e
