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

    @classmethod
    def get_journal(cls):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM journal"
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return results

    @classmethod
    def get_year_by_name(cls, name):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT year FROM journal WHERE name = '%s' " % name
        mycursor.execute(sql)
        results = mycursor.fetchall()
        year = []
        for i in range(len(results)):
            year.append(results[i][0])
        mycursor.close()
        mydb.close()
        return year

    @classmethod
    def get_stage_by_nameandyear(cls, name, year):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT stage FROM journal WHERE name = '%s' AND year='%d'" % (name, year)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        stage = []
        for i in range(len(results)):
            stage.append(results[i][0])
        mycursor.close()
        mydb.close()
        return stage

    @classmethod
    def get_journal_by_stage(cls, name, year, stage):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM journal WHERE name = '%s' AND year='%d' AND stage='%d'" % (name, year, stage)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return results


if __name__ == '__main__':
    print(JournalDB.get_journal_by_stage('science', 1999, 1))
