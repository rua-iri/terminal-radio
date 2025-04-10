import sqlite3
import time


class DB_DAO:

    def __init__(self):
        self.connection = sqlite3.connect("resource/radio_sources.sqlite")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def select_all_stations(self) -> list[dict]:
        station_list = []
        query_string: str = "SELECT name, url, img, is_yt FROM stations"
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

    def update_station(self,
                       id: int,
                       name: str,
                       url: str,
                       img: str,
                       is_yt: bool,
                       is_active: bool
                       ):
        query_string: str = """UPDATE stations
        SET name=?, url=?, img=?, is_yt=?, is_active=?
        WHERE id=?"""

        self.cursor.execute(
            query_string,
            (name, url, img, is_yt, is_active, id, )
        )

    def delete_station(self, id: int):
        query_string: str = "DELETE FROM stations WHERE id=?"

        self.cursor.execute(query_string, (id, ))
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

    def get_last_station(self) -> int:
        query_string: str = """SELECT *
        FROM last_station
        INNER JOIN stations
        ON last_station.station_id = stations.id
        ORDER BY last_station.id DESC
        LIMIT 1;"""

        result = self.cursor.execute(query_string, ())

        return result.fetchone()['id']

    def set_last_station(self, id: int) -> None:
        query_string: str = """
        INSERT INTO last_station
        (station_id, timestamp)
        VALUES
        (?, ?);
        """
        timestamp = int(time.time())

        print(id)
        print(timestamp)

        self.cursor.execute(query_string, (id, timestamp))
        self.connection.commit()


# For testing, remove later
a = DB_DAO()


a.set_last_station(12)
