import datetime
import time
from database.db_base import DBBase


class RecordDB(DBBase):
    @classmethod
    def add_order(cls, account, key):
        """
        插入预约记录
        :param account: 用户账户
        :param key: 期刊标识
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        order_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        sql = "INSERT INTO record (account,key,order_time,order_flag,borrow_flag,return_flag) " \
              "VALUES ('%s','%s','%s',1,0,0)" % (account, key, order_time)
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()

    @classmethod
    def add_borrow(cls, account, key):
        """
        插入直接借阅记录
        :param account: 用户账户
        :param key: 期刊标识
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        borrow_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        sql = "INSERT INTO record (account,key,borrow_time,order_flag,borrow_flag,return_flag) " \
              "VALUES ('%s','%s','%s',0,1,0)" % (account, key, borrow_time)
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()

    @classmethod
    def update_borrow_time(cls, account, key, order_time):
        """
        预约后借阅
        :param account: 用户账户
        :param key: 期刊标识
        :param order_time: 预订时间
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        borrow_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        sql = "UPDATE record SET borrow_time='%s'  Where account = '%s' AND key='%s' AND order_time='%s'" % (
            borrow_time, account, key, order_time)
        mycursor.execute(sql)
        sql = "UPDATE record SET borrow_flag= 1  Where account = '%s' AND key='%s' AND order_time='%s'" % (
            account, key, order_time)
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()

    @classmethod
    def update_return_time(cls, account, key, borrow_time):
        """
        归还期刊
        :param account: 用户账户
        :param key: 期刊标识
        :param borrow_time: 借阅时间
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        return_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        sql = "UPDATE record SET return_time='%s',return_flag = 1 Where account = '%s' AND key='%s' AND " \
              "borrow_time='%s'" % (return_time, account, key, borrow_time)
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()

    @classmethod
    def get_record_by_account(cls, account):
        """
        查询用户借阅信息
        :param account: 用户账户
        :return: 该用户所有借阅记录
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM record WHERE account = '%s' " % account
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return results

    @classmethod
    def get_key_by_account(cls, account):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT key FROM record WHERE account = '%s' " % account
        mycursor.execute(sql)
        results = mycursor.fetchall()
        key = []
        for row in results:
            key.append(row[0])
        mycursor.close()
        mydb.close()
        return key

    @classmethod
    def get_info_length(cls, account):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT key FROM record WHERE account  = '%s'" % account
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return len(results)

    @classmethod
    def get_this_day_record_num(cls, date: str, choice: str):
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = ""
        if choice == 'order':
            sql = "SELECT COUNT(*) AS this_day_order_num FROM record WHERE order_time LIKE '" + date + "%'"
        elif choice == 'borrow':
            sql = "SELECT COUNT(*) AS this_day_order_num FROM record WHERE borrow_time LIKE '" + date + "%'"
        elif choice == 'return':
            sql = "SELECT COUNT(*) AS this_day_order_num FROM record WHERE return_time LIKE '" + date + "%'"
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return results[0][0]

    @classmethod
    def datetime_to_str(cls, date_time):
        return datetime.datetime.strftime(date_time, '%Y%m%d%H%M%S')

    @classmethod
    def str_to_datetime(cls, str1):
        return datetime.datetime.strptime(str1, '%Y%m%d%H%M%S')


if __name__ == '__main__':
    print()
    pass
