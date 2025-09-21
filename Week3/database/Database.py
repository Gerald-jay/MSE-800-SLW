import sqlite3
from dataclasses import dataclass, field

@dataclass
class Database:
    conn: sqlite3.Connection = field(init=False)
    cur: sqlite3.Cursor = field(init=False)

    def connect_data(self, sql: str):
        self.conn = sqlite3.connect(sql)
        self.cur = self.conn.cursor()

    def create_table(self, sql: str):
        self.cur.execute(sql)

        #"""
        #CREATE TABLE IF NOT EXISTS Student (
         #   user_id INTEGER PRIMARY KEY,
          #  class_id INTEGER
           # name TEXT NOT NULL,
            #email TEXT UNIQUE
       # )
        #"""
    
    def add_data(self, sql: str):
        self.cur.execute(sql)

    def find_data(self, sql: str):
        self.cur.execute(sql)

    def commit_data(self):
        self.conn.commit()

    def close_connect(self):
        self.conn.close()