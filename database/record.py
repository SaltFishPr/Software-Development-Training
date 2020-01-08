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
        order_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        sql = "INSERT INTO record (account,key,order_time,order_flag,borrow_flag,return_flag) " \
              "VALUES ('%s','%s','%s',1,0,0)" % (account, key, order_time)
        cls._execute_sql(RecordDB(), sql, 'insert')

    @classmethod
    def add_borrow(cls, account, key):
        """
        插入直接借阅记录
        :param account: 用户账户
        :param key: 期刊标识
        :return:
        """
        borrow_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        sql = "INSERT INTO record (account,key,borrow_time,order_flag,borrow_flag,return_flag) " \
              "VALUES ('%s','%s','%s',0,1,0)" % (account, key, borrow_time)
        cls._execute_sql(RecordDB(), sql, 'insert')

    @classmethod
    def update_borrow_time(cls, account, key, order_time):
        """
        预约后借阅
        :param account: 用户账户
        :param key: 期刊标识
        :param order_time: 预订时间
        :return:
        """
        borrow_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        sql = "UPDATE record SET borrow_time = '%s', borrow_flag = 1  Where account = '%s' AND key = %d AND " \
              "order_time = '%s'" % (borrow_time, account, key, order_time)
        cls._execute_sql(RecordDB(), sql, 'update')

    @classmethod
    def update_return_time(cls, account, key, borrow_time):
        """
        归还期刊
        :param account: 用户账户
        :param key: 期刊标识
        :param borrow_time: 借阅时间
        :return:
        """
        return_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        sql = "UPDATE record SET return_time='%s',return_flag = 1 Where account = '%s' AND key='%s' AND " \
              "borrow_time='%s'" % (return_time, account, key, borrow_time)
        cls._execute_sql(RecordDB(), sql, 'update')

    @classmethod
    def get_record_by_account(cls, account):
        """
        查询用户借阅信息
        :param account: 用户账户
        :return: 该用户所有借阅记录
        """
        sql = "SELECT * FROM record WHERE account = '%s' " % account
        results = cls._execute_sql(RecordDB(), sql, 'select')
        return results

    @classmethod
    def get_key_by_account(cls, account):
        sql = "SELECT key FROM record WHERE account = '%s' " % account
        results = cls._execute_sql(RecordDB(), sql, 'select')
        key = []
        for row in results:
            key.append(row[0])
        return key

    @classmethod
    def get_this_day_record_num(cls, date: str, choice: str):
        sql = ""
        if choice == 'order':
            sql = "SELECT COUNT(*) AS this_day_order_num FROM record WHERE order_time LIKE '" + date + "%'"
        elif choice == 'borrow':
            sql = "SELECT COUNT(*) AS this_day_order_num FROM record WHERE borrow_time LIKE '" + date + "%'"
        elif choice == 'return':
            sql = "SELECT COUNT(*) AS this_day_order_num FROM record WHERE return_time LIKE '" + date + "%'"
        results = cls._execute_sql(RecordDB(), sql, 'select')
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
