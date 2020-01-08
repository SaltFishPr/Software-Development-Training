from database.db_base import DBBase
from database.record import RecordDB


class JournalDB(DBBase):
    @classmethod
    def insert_journal(cls, year, stage, name, tags, stock_num, order_num, lend_num, total_num, issn='default',
                       press='defalut', editor='default'):
        sql = "INSERT INTO journal (issn, year, stage, name, tag, stock_num, order_num, lend_num, total_num, press," \
              " editor) values ('%s',%d,%d,'%s','%s',%d,%d,%d,%d,'%s','%s')" % (
                  issn, year, stage, name, tags, stock_num, order_num, lend_num, total_num, press, editor)
        cls._execute_sql(JournalDB(), sql, 'insert')

    @classmethod
    def remove_journal(cls, name, year, stage):
        sql = "DELETE FROM journal WHERE name = '%s'AND year =%d AND stage =%d " % (name, year, stage)
        cls._execute_sql(JournalDB(), sql, 'delete')

    @classmethod
    def get_stage_by_name_year(cls, name, year):
        """
        查询  该期刊名，该年  的期刊
        :param name:
        :param year:
        :return:
        """
        sql = "SELECT stage FROM journal WHERE name = '%s' AND year='%d'" % (name, year)
        results = cls._execute_sql(JournalDB(), sql, 'select')
        stage = []
        for i in range(len(results)):
            stage.append(results[i][0])
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
        sql = "SELECT * FROM journal WHERE name = '%s' AND year='%d' AND stage='%d'" % (name, year, stage)
        results = cls._execute_sql(JournalDB(), sql, 'select')
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
        sql = "SELECT key FROM journal WHERE name = '%s' AND year='%d' AND stage='%d'" % (name, year, stage)
        results = cls._execute_sql(JournalDB(), sql, 'select')
        return results[0][0]

    @classmethod
    def get_name_by_key(cls, key):
        """

        :param key:
        :return:
        """
        sql = "SELECT name FROM journal WHERE key = %d " % key
        results = cls._execute_sql(JournalDB(), sql, 'select')
        name = results[0][0]
        return name

    @classmethod
    def get_year_by_key(cls, key):
        """

        :param key:
        :return:
        """
        sql = "SELECT year FROM journal WHERE key = '%d' " % key
        results = cls._execute_sql(JournalDB(), sql, 'select')
        year = results[0][0]
        return year

    @classmethod
    def get_stage_by_key(cls, key):
        """

        :param key:
        :return:
        """
        sql = "SELECT stage FROM journal WHERE key = '%d' " % key
        results = cls._execute_sql(JournalDB(), sql, 'select')
        stage = results[0][0]
        return stage

    @classmethod
    def update_journal_num(cls, key, stock_num, order_num, lend_num, total_num):
        sql = "UPDATE journal SET stock_num = %d , order_num= %d , lend_num = %d ,total_num = %d WHERE key = %d" % (
            stock_num, order_num, lend_num, total_num, key)
        cls._execute_sql(JournalDB(), sql, 'update')

    @classmethod
    def search_journal(cls, str1: str):
        sql = "SELECT * FROM journal WHERE name LIKE " + r"'%" + str1.capitalize() + r"%'" + " OR " + r"'%" + str1.lower() + r"%'"
        results = cls._execute_sql(JournalDB(), sql, 'select')
        return results


if __name__ == '__main__':
    print(JournalDB.search_journal('fuzzy'))
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
