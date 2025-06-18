import pytest

from terminal_radio.classes import Station


def test_create_station():
    assert True is True
    station = Station(
        "Test Station", "https://example.com", "https://example.com", False
    )

    assert type(station) is Station

    assert station.is_yt is False
    assert station.name == "Test Station"
    assert station.url == "https://example.com"
    assert station.img == "https://example.com"
