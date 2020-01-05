from database import db_init
import time


# 插入预约记录
def add_order(account, key):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    order_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "INSERT INTO record (account,key,order_time,order_flag,borrow_flag,return_flag) " \
          "VALUES ('%s','%s','%s',1,0,0)" % (account, key, order_time)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


# 插入直接借阅
def add_borrow(account, key):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    borrow_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "INSERT INTO record (account,key,borrow_time,order_flag,borrow_flag,return_flag) " \
          "VALUES ('%s','%s','%s',0,1,0)" % (account, key, borrow_time)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


# 更新借阅时间
def update_borrow_time(account, key, order_time):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    borrow_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "UPDATE record SET borrow_time='%s'  Where account = '%s' AND key='%s' AND order_time='%s'" % (
        borrow_time, account, key, order_time)
    mycursor.execute(sql)
    sql = "UPDATE record SET borrow_flag= 1  Where account = '%s' AND key='%s' AND order_time='%s'" % (
        account, key, order_time)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


# 更新归还时间
def update_return_time(account, key, borrow_time):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    return_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "UPDATE record SET return_time='%s' Where account = '%s' AND key='%s' AND borrow_time='%s'" % (
        return_time, account, key, borrow_time)
    mycursor.execute(sql)
    sql = "UPDATE record SET return_flag=1 Where account = '%s' AND key='%s' AND borrow_time='%s'" % (
        account, key, borrow_time)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


# 查询记录
def ask_record(account, key, order_flag, borrow_flag, return_flag):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "SELECT * FROM record WHERE account = '%s' AND key='%s' AND order_flag='%s' AND borrow_flag='%s' AND return_flag='%s'" % (
        account, key, order_flag, borrow_flag, return_flag)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return results


# 用户借阅信息查询
def ask_record_by_account(account):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "SELECT * FROM record WHERE account = '%s' " % (account)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return results


def ask_key_by_account(account):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "SELECT key FROM Record WHERE account = '%s' " % (account)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    key = []
    for row in results:
        key.append(row[0])
    mycursor.close()
    mydb.close()
    return key


def get_info_account(account):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "SELECT key FROM Record WHERE account  = '%s'" % (account)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return len(results)


if __name__ == '__main__':
    pass
