import sqlite3
import time


class DB_DAO:

    def __init__(self):
        self.connection = sqlite3.connect("resource/radio_sources.sqlite")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def select_all_stations(self) -> list[dict]:
        station_list = []
        query_string: str = """SELECT name,
        url, img, is_yt
        FROM stations
        WHERE is_active=1"""

        result = self.cursor.execute(query_string)
        results = result.fetchall()

        for item in results:
            station_list.append({**item})

        return station_list

    def select_station_by_id(self, id: int) -> dict:
        query_string: str = "SELECT * FROM stations WHERE id=?"
        result = self.cursor.execute(query_string, (id, ))
        results = result.fetchone()

        return {**results}

    def get_station_id(self, name: str) -> int:
        query_string = "SELECT id FROM stations WHERE name = ?;"
        result = self.cursor.execute(query_string, (name,))

        return result.fetchone()['id']

    def update_station(self,
                       id: int,
                       name: str,
                       url: str,
                       img: str,
                       is_yt: bool,
                       ):
        query_string: str = """UPDATE stations
        SET name=?, url=?, img=?, is_yt=?
        WHERE id=?"""

        self.cursor.execute(
            query_string,
            (name, url, img, is_yt, id, )
        )
        self.connection.commit()

    def delete_station(self, name: str):
        query_string: str = """UPDATE stations
        SET is_active=0
        WHERE name=?"""

        self.cursor.execute(query_string, (name, ))
        self.connection.commit()

    def create_station(self,
                       name: str,
                       url: str,
                       img: str,
                       is_yt: bool,
                       ):
        query_string: str = """INSERT INTO
        stations (name, url, img, is_yt, is_active)
        VALUES (?, ?, ?, ?, ?)"""

        self.cursor.execute(query_string, (name, url, img, is_yt, True))
        self.connection.commit()

    def get_last_station(self) -> str:
        query_string: str = """SELECT stations.name
        FROM last_station
        INNER JOIN stations
        ON last_station.station_id = stations.id
        ORDER BY last_station.id DESC
        LIMIT 1;"""

        result = self.cursor.execute(query_string, ())

        item = result.fetchone()

        if item:
            return item

        return None

    def set_last_station(self, id: int) -> None:
        query_string: str = """
        INSERT INTO last_station
        (station_id, timestamp)
        VALUES
        (?, ?);
        """
        timestamp = int(time.time())

        self.cursor.execute(query_string, (id, timestamp))
        self.connection.commit()


if __name__ == "__main___":
    # For testing, remove later
    a = DB_DAO()

    # a.set_last_station(12)
    x = a.get_station_id("RTE Raidio Na Gaeltachta")
    print(x)
