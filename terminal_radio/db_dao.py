import sqlite3


class DB_DAO:

    def __init__(self):
        connection = sqlite3.connect("resource/radio_sources.sqlite")
        connection.row_factory = sqlite3.Row
        self.cursor = connection.cursor()

    def select_all_stations(self):
        query_string: str = "SELECT id, name FROM stations"
        result = self.cursor.execute(query_string)
        return result.fetchall()

    def select_station_by_id(self, id: int):
        print(1)
        query_string: str = "SELECT * FROM stations WHERE id="
        print(2)
        result = self.cursor.execute(query_string, (id, ))
        print(3)
        return result.fetchone()


a = DB_DAO()

x = a.select_all_stations()
for z in x:
    print(z['name'])

y = a.select_station_by_id(id=10)
print(y)
