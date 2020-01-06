from database.db_base import DBBase


class JournalDB(DBBase):
    @classmethod
    def get_name_by_key(cls, key):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT name FROM journal WHERE key = '%d' " % key
        mycursor.execute(sql)
        results = mycursor.fetchall()
        name = results[0][0]
        mycursor.close()
        mydb.close()
        return name


if __name__ == '__main__':
    pass
