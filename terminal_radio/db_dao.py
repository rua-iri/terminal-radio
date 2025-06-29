import sqlite3
import time


class DB_DAO:

    def __init__(self):
        self.connection = sqlite3.connect("resource/radio_sources.sqlite")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def get_all_stations(self) -> list[dict]:
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

    def get_last_station(self) -> str | None:
        query_string: str = """SELECT stations.name
        FROM last_station
        INNER JOIN stations
        ON last_station.station_id = stations.id
        ORDER BY last_station.id DESC
        LIMIT 1;"""

        result = self.cursor.execute(query_string, ())

        item = result.fetchone()

        if item:
            return item['name']

        return None

    def set_last_station(self, name: str) -> None:
        current_station_id = self.get_station_id(name)

        insert_query_string: str = """
        INSERT INTO last_station
        (station_id, timestamp)
        VALUES
        (?, ?);
        """
        timestamp = int(time.time())

        self.cursor.execute(insert_query_string,
                            (current_station_id, timestamp)
                            )
        self.connection.commit()

    def get_stats_top_5(self):
        select_query_string: str = """
        SELECT stations.name as 'Station Name',
        count(last_station.id) AS "Play Count"
        FROM last_station
        INNER JOIN stations
        ON last_station.station_id = stations.id
        GROUP BY station_id
        ORDER BY "Play Count" DESC
        LIMIT 5;
        """

        result = self.cursor.execute(select_query_string)

        return result.fetchall()

    def close(self):
        self.connection.close()
