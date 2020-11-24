from enum import Enum
import sqlite3


class FETCH_TYPE(Enum):
    ONE = 1,
    ALL = 2,


class DatabaseManager:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

    def execute(self, command, args=[], after_commit=False):
        self.cursor.execute(command, args)
        if after_commit:
            self.commit()

    def commit(self):
        self.conn.commit()

    def fetch(self, type=FETCH_TYPE.ALL):
        return self.cursor.fetchone() if type == FETCH_TYPE.ONE else self.cursor.fetchall()

    def __del__(self):
        self.conn.close()


class RecentFilesManager:
    def __init__(self, filename="./database/last_files.db"):
        print(filename)
        self.db_manager = DatabaseManager(filename)

    def write_recent_file(self, path):
        self.db_manager.execute("DELETE FROM last_files WHERE path=?", [path])
        self.db_manager.execute("INSERT INTO last_files (path) VALUES(?)", [path], after_commit=True)

    def get_recent_files(self):
        query = "SELECT path FROM last_files LIMIT 10"
        self.db_manager.execute(query)
        return self.db_manager.fetch()

    def clear_recent_files(self):
        query = "DELETE FROM last_files"
        self.db_manager.execute(query, after_commit=True)
