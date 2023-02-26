import sqlite3
from sqlite3 import Error
from typing import List


class SQLiteWrapper:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def create_connection(self, path: str) -> sqlite3.Connection:
        try:
            self.conn = sqlite3.connect(path)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Connect: {e=}")
        return self.conn

    def execute_query(self, query: str, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Error as e:
            print(f"Execute: {e=}, \nQuery: {query=}")

    def execute_multiparam_query(self, query: str, params: List[tuple]):
        try:
            self.cursor.executemany(query, params)
            self.conn.commit()
        except Error as e:
            print(f"Execute: {e=}, \nQuery: {query=}")

    def execute_read_query(self, query: str):
        result = None
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"Read: {e=}")

    def read_sql_file(self, path: str) -> str:
        fd = open(path, "r")
        content = fd.read()
        fd.close()
        return content
