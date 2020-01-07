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
        查询所有期刊
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
        查询  该期刊名  的期刊
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
        查询  该期刊名，该年  的期刊
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
        根据  名字，年份，期  得到唯一期刊
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
        得到该  名字，年份，期  期刊的key
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

    @classmethod
    def get_journal_name_year_stage(cls,key):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM journal WHERE key = '%d' " % (key)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        journal_name_year_stage=results[0][4]+"-"+str(results[0][2])+"-"+str(results[0][3])
        mycursor.close()
        mydb.close()
        return journal_name_year_stage

if __name__ == '__main__':
    pass
    print(JournalDB.get_journal_name_year_stage(1))
    # print(JournalDB.get_journal_by_stage('science', 1999, 1))
