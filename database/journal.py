from database.db_base import DBBase


class JournalDB(DBBase):
    @classmethod
    def get_name_by_key(cls, key):
        """

        :param key:
        :return:
        """
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
        """

        :return:
        """
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
        """

        :param name:
        :return:
        """
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
    def get_stage_by_name_and_year(cls, name, year):
        """

        :param name:
        :param year:
        :return:
        """
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
        """

        :param name:
        :param year:
        :param stage:
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM journal WHERE name = '%s' AND year='%d' AND stage='%d'" % (name, year, stage)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return results

    @classmethod
    def get_key(cls, name, year, stage):
        """

        :param name:
        :param year:
        :param stage:
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT key FROM journal WHERE name = '%s' AND year='%d' AND stage='%d'" % (name, year, stage)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return results[0][0]


if __name__ == '__main__':
    pass
    dict_test = {
        'name': 'nature'
    }
    print(JournalDB.get_info_by_dict("journal", dict_test))
    # print(JournalDB.get_journal_by_stage('science', 1999, 1))
