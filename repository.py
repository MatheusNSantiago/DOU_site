import mysql.connector
import json
from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection

from model import Publicacao

class SumulaDB:
    def __init__(self, is_local=True):
        if is_local:
            self._conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="oasuet10",
                database="dou_db_local",
            )
        else:
            with open("credentials.json", "r") as f:
                cred = json.loads(f.read())

                self._conn = mysql.connector.connect(
                    host=cred["ENDPOINT"],
                    user=cred["USER"],
                    password=cred["PASSWORD"],
                    database=cred["DATABASE"],
                )

        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()

    @property
    def connection(self) -> MySQLConnection:
        return self._conn

    @property
    def cursor(self) -> MySQLCursor:
        return self._cursor

    def commit(self):
        self.connection.commit()

    def _close(self, commit=False):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def _fetchall(self):
        resp = [Publicacao(*pub) for pub in self.cursor.fetchall()]
        return resp
    
    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self._fetchall()
