
from terminal_radio.db_dao import DB_DAO


db_dao = DB_DAO()


def test_get_all_stations():
    all_stations = db_dao.get_all_stations()

    assert type(all_stations) is list
    assert len(all_stations) > 0


def test_get_last_station():
    last_station = db_dao.get_last_station()

    assert type(last_station) is str or type(last_station) is None
