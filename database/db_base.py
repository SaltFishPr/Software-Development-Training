import sqlite3
import os
import random

database_path = os.path.dirname(__file__) + '/PMS'


class DBBase(object):
    @classmethod
    def get_info_by_dict(cls, table_name, args: dict):
        """
        根据传入的参数自动生成sql语句来查询
        :param table_name: 表名
        :param args: 传入dict，是tables
        :return: 根据选项获得表的所有信息
        """
        if args == {}:
            sql = "SELECT * FROM " + table_name
        else:
            sql1 = "SELECT * FROM " + table_name + " WHERE "
            keys = list(args.keys())
            values = list(args.values())
            sql2 = ""
            # 前面的参数后面要加AND
            for i in range(len(args) - 1):
                if isinstance(values[i], str):
                    sql2 = sql2 + keys[i] + " = \'" + values[i] + "\' AND "
                elif isinstance(values[i], int):
                    sql2 += keys[i] + " = " + str(values[i]) + " AND "
            # 最后一个参数后面不加AND
            if isinstance(values[-1], str):
                sql2 += keys[-1] + " = \'" + values[-1] + '\''
            elif isinstance(values[-1], int):
                sql2 += keys[-1] + " = " + str(values[-1])
            sql = sql1 + sql2
        results = cls._execute_sql(DBBase(), sql, 'select')
        res = []
        for temp in results:
            res.append(list(temp))
        return res

    def _execute_sql(self, sql, choice):
        """
        执行sql语句
        :param sql:
        :param choice: 'select'， 'update', 'insert', 'delete'
        :return:
        """
        my_db = sqlite3.connect(database_path)
        my_cursor = my_db.cursor()
        my_cursor.execute(sql)
        results = []
        if choice == 'select':
            results = my_cursor.fetchall()
        else:
            my_db.commit()
        my_cursor.close()
        my_db.close()
        return results

    @classmethod
    def generate_journal_info(cls):
        name_dicts = [
            {'issn': '0036-8075', 'name': 'Science', 'tag': '科学', 'press': '美国科学促进会', 'editor': 'Marcia McNutt'},
            {'issn': '1476-4687', 'name': 'Nature', 'tag': '科学', 'press': '美国科学促进会', 'editor': 'No'},
            {'issn': '0893-6080', 'name': 'Neural Networks', 'tag': '人工智能', 'press': 'press_test',
             'editor': 'editor_test'},
            {'issn': '1566-2535', 'name': 'Information Fusion', 'tag': '人工智能', 'press': 'press_test',
             'editor': 'editor_test'},
            {'issn': '2168-2267', 'name': 'IEEE Transactions on Cybernetics', 'tag': '人工智能', 'press': 'press_test',
             'editor': 'editor_test'},
            {'issn': '1613-6810', 'name': 'small', 'tag': '化学', 'press': 'press_test', 'editor': 'editor_test'},
            {'issn': '0005-1098', 'name': 'Automatic', 'tag': '自动化', 'press': 'press_test', 'editor': 'editor_test'},
            {'issn': '0142-9612', 'name': 'Biomaterials', 'tag': '生物医学', 'press': 'press_test',
             'editor': 'editor_test'},
            {'issn': '2095-8009', 'name': 'Engineering', 'tag': '综合', 'press': 'press_test', 'editor': 'editor_test'},
            {'issn': '2169-5172', 'name': 'Soft Robotics', 'tag': '机器人学', 'press': 'press_test',
             'editor': 'editor_test'}]

        res = []
        for i in range(150):
            info = name_dicts[random.randint(0, 9)]
            year = random.randint(1999, 2020)
            stage = random.randint(1, 12)
            sql = "INSERT INTO journal (issn, year, stage, name, tag, stock_num, order_num, lend_num, total_num, press," \
                  " editor) values ('%s',%d,%d,'%s','%s',%d,%d,%d,%d,'%s','%s')" % (
                      info['issn'], year, stage, info['name'], info['tag'], 100, 0, 0, 100, info['press'],
                      info['editor'])
            res.append(sql)
        res = list(set(res))
        for temp in res:
            cls._execute_sql(DBBase(), temp, 'insert')


if __name__ == '__main__':
    # get_info_dict = {
    #     'account': 'jl'
    # }
    # print(DBBase.get_info_by_dict('user', get_info_dict))
    DBBase.generate_journal_info()
    pass
