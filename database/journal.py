from database.db_base import DBBase
from database.record import RecordDB

class JournalDB(DBBase):
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
    def get_stage_by_name_year(cls, name, year):
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
    def get_journal_by_name_year_stage(cls, name, year, stage):
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
    def get_journal_name_year_stage(cls, key):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM journal WHERE key = '%d' " % key
        mycursor.execute(sql)
        results = mycursor.fetchall()
        journal_name_year_stage = results[0][4] + "-" + str(results[0][2]) + "-" + str(results[0][3])
        mycursor.close()
        mydb.close()
        return journal_name_year_stage

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
    def get_year_by_key(cls, key):
        """

        :param key:
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT year FROM journal WHERE key = '%d' " % key
        mycursor.execute(sql)
        results = mycursor.fetchall()
        year = results[0][0]
        mycursor.close()
        mydb.close()
        return year

    @classmethod
    def get_stage_by_key(cls, key):
        """

        :param key:
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT stage FROM journal WHERE key = '%d' " % key
        mycursor.execute(sql)
        results = mycursor.fetchall()
        stage = results[0][0]
        mycursor.close()
        mydb.close()
        return stage

    @classmethod
    def update_journal_num(cls, key, stock_num, order_num, lend_num, total_num):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "UPDATE journal SET stock_num = %d , order_num= %d , lend_num = %d ,total_num = %d WHERE key = %d" % (
            stock_num, order_num, lend_num, total_num, key)
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()

    @classmethod
    def search_journal(cls, str1):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM journal WHERE name like " + r"'%" + str1 + r"%'"
        print(sql)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return results


if __name__ == '__main__':
    pass
    # journal_info = JournalDB.get_journal_by_name_year_stage('science', 1999, 1)
    # get_record_dict = {
    #     'account': 'jl',
    #     'key': 1,
    #     'borrow_flag': 1
    # }
    # result = RecordDB.get_info_by_dict('record', get_record_dict)
    # result.sort(key=lambda x: x[3])
    # RecordDB.update_return_time('jl', 1, result[0][3])
    # JournalDB.update_journal_num(1, journal_info[0][6] + 1, journal_info[0][7], journal_info[0][8] - 1,
    #                              journal_info[0][9])
