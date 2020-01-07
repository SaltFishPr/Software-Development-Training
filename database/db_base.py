import sqlite3
import os

database_path = os.path.dirname(__file__) + '/PMS'


class DBBase(object):

    @classmethod
    def connect(cls):
        my_db = sqlite3.connect(database_path)
        return my_db

    @classmethod
    def get_info_by_dict(cls, table_name, args: dict):
        """
        根据传入的参数自动生成sql语句来查询
        :param table_name: 表名
        :param args: 传入dict，是tables
        :return: 根据选项获得表的所有信息
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
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
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        res = []
        for temp in results:
            res.append(list(temp))
        return res


if __name__ == '__main__':
    # print(database_path)
    print(DBBase.get_info_by_dict('user', {'account': 'jl'}))
