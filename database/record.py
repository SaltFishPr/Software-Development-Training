from database import db_init
import time

#插入预约记录
def add_order(account, key):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    order_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "INSERT INTO Record (account,key,order_time,order_flag,borrow_flag,return_flag) " \
          "VALUES ('%s','%s','%s',1,0,0)"%(account,key,order_time)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()

#插入直接借阅
def add_borrow(account,key):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    borrow_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "INSERT INTO Record (account,key,borrow_time,order_flag,borrow_flag,return_flag) " \
          "VALUES ('%s','%s','%s',0,1,0)"%(account,key,borrow_time)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()

#
def update_borrow_time(account,key,order_time):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    borrow_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "UPDATE Record SET borrow_time='%s'  Where account = '%s' AND key='%s' AND order_time='%s'"%(borrow_time,account,key,order_time)
    mycursor.execute(sql)
    sql = "UPDATE Record SET borrow_flag= 1  Where account = '%s' AND key='%s' AND order_time='%s'"%(account,key,order_time)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()

def UpdateReturn_time(account,key,borrow_time):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    return_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "UPDATE Record SET return_time='%s' Where account = '%s' AND key='%s' AND borrow_time='%s'"%(return_time,account,key,borrow_time)
    mycursor.execute(sql)
    sql = "UPDATE Record SET return_flag=1 Where account = '%s' AND key='%s' AND borrow_time='%s'" % (account, key, borrow_time)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()

def AskRecord(account,key,order_flag,borrow_flag,return_flag):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql="SELECT * FROM Record WHERE account = '%s' AND key='%s' AND order_flag='%s' AND borrow_flag='%s' AND return_flag='%s'"%(account,key,order_flag,borrow_flag,return_flag)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return results




if __name__ == '__main__':
    result=AskRecord('123',1,1,1,1)
    print(result)