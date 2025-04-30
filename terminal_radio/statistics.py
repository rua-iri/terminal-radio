

from terminal_radio.db_dao import DB_DAO
from tabulate import tabulate


def show_table(stats_list: list):
    headers = stats_list[0].keys()
    table = tabulate(stats_list, headers=headers, tablefmt="fancy_grid")
    print(table)


def main():
    db_dao = DB_DAO()
    top_5_stations = db_dao.get_stats_top_5()

    show_table(top_5_stations)

    db_dao.close()
