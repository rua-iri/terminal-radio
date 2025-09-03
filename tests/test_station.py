
from terminal_radio.classes import Station
import re

def test_create_station():
    assert True is True
    station = Station(
        name="Test Station",
        url="https://example.com",
        img="https://example.com",
        is_yt=False
    )

    assert type(station) is Station

    assert station.is_yt is False
    assert station.name == "Test Station"
    assert station.url == "https://example.com"
    assert station.img == "https://example.com"


def test_create_station_yt():
    initial_station_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    station = Station(
        name="Test Station",
        url=initial_station_url,
        img="",
        is_yt=True
    )

    print(station.url)

    URL_PATTERN = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.googlevideo\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

    assert station.url != initial_station_url
    assert station.img != ""
    assert re.match(pattern=URL_PATTERN, string=station.url)
