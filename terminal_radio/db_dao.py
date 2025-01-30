import sqlite3


class DB_DAO:

    def __init__(self):
        connection = sqlite3.connect("resource/radio_sources.sqlite")
        connection.row_factory = sqlite3.Row
        self.cursor = connection.cursor()

    def select_all_stations(self) -> list[sqlite3.Row]:
        query_string: str = "SELECT id, name FROM stations"
        result = self.cursor.execute(query_string)
        return result.fetchall()

    def select_station_by_id(self, id: int) -> sqlite3.Row:
        query_string: str = "SELECT * FROM stations WHERE id=?"
        result = self.cursor.execute(query_string, (id, ))
        return result.fetchone()

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


# For testing, remove later
a = DB_DAO()

x = a.select_all_stations()
for z in x:
    print(z['name'])

y = a.select_station_by_id(id=10)
print(y)
print({**y})
