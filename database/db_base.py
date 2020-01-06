import sqlite3
import os

database_path = os.path.dirname(__file__) + r'\PMS'
print(database_path)


class DBBase(object):

    @classmethod
    def connect(cls):
        my_db = sqlite3.connect(database_path)
        return my_db
