from enum import Enum
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class FetchType(Enum):
    ONE = 1,
    ALL = 2,


class ResultType(Enum):
    TUPLE = 1,
    DICT = 2,


class DatabaseManager:
    def __init__(self, filename: str, type_: ResultType = ResultType.TUPLE):
        self.conn = sqlite3.connect(filename)
        self.result_type = type_
        if type_ == ResultType.DICT:
            self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()

    def execute(self, command: str, args=[], after_commit=False):
        self.cursor.execute(command, args)
        if after_commit:
            self.commit()

    def commit(self):
        self.conn.commit()

    def fetch(self, type: FetchType = FetchType.ALL):
        return self.cursor.fetchone() if type == FetchType.ONE else self.cursor.fetchall()

    def result_type(self) -> ResultType:
        return self.result_type

    def __del__(self):
        self.conn.close()


class RecentFilesManager:
    def __init__(self, filename: str = "./resources/last_files.db"):
        self.db_manager = DatabaseManager(filename)

    def write_recent_file(self, path: str):
        self.db_manager.execute("DELETE FROM last_files WHERE path=?", [path])
        self.db_manager.execute("INSERT INTO last_files (path) VALUES(?)", [path], after_commit=True)

    def get_recent_files(self):
        query = "SELECT path FROM last_files LIMIT 10"
        self.db_manager.execute(query)
        return self.db_manager.fetch()

    def clear_recent_files(self):
        query = "DELETE FROM last_files"
        self.db_manager.execute(query, after_commit=True)
