# -*- coding: utf-8 -*-
import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_users(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM users').fetchall()

    def add_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT id FROM users WHERE user_id='" + str(user_id) + "'").fetchall()
            if len(result) == 0:
                self.cursor.execute('INSERT INTO users(user_id) VALUES (' + str(user_id) + ')')
            else:
                return False

    def delete_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT id FROM users WHERE user_id='" + str(user_id) + "'").fetchall()
            if len(result) != 0:
                self.cursor.execute("DELETE FROM users WHERE user_id='" + str(user_id) + "'")
            else:
                return False

    def close(self):
        self.connection.close()
