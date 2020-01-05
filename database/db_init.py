import sqlite3
import os

database_path=os.path.dirname(__file__)+r'\PMS'
print(database_path)
def connect():
    mydb = sqlite3.connect(database_path)
    return mydb

def creat_user_table():
    mydb=connect()
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE User ("
                     "account VARCHAR(20) PRIMARY KEY,"
                     "password VARCHAR(20),"
                     "name VARCHAR(255),"
                     "identity VARCHAR(20),"
                     "grade TINYINT)")
    mycursor.close()
    mydb.close()

def del_user_table():
    mydb = connect()
    mycursor = mydb.cursor()
    sql = "DROP TABLE IF EXISTS User"
    mycursor.execute(sql)
    mycursor.close()
    mydb.close()

def creat_periodical_table():
    mydb=connect()
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE Periodical ("
                     "key INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "issn VARCHAR(20),"
                     "year INT,"
                     "stage INT,"
                     "name VARCHAR(255),"
                     "tage VARCHAR(65535),"
                     "stock_num INT,"
                     "oder_num INT,"
                     "lend_num INT,"
                     "total_num INT,"
                     "press VARCHAR(255),"
                     "editor VARCHAR(255))")
    mycursor.close()
    mydb.close()

def del_periodical_table():
    mydb =connect()
    mycursor = mydb.cursor()
    sql = "DROP TABLE IF EXISTS Periodical"
    mycursor.execute(sql)
    mycursor.close()
    mydb.close()

def creat_record_table():
    mydb=connect()
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE Record ("
                     "account VARCHAR(20),"
                     "key INTEGER PRIMARY KEY,"
                     "order_time VARCHAR(20),"
                     "borrow_time VARCHAR(20),"
                     "return_time VARCHAR(20),"
                     "order_flag INT,"
                     "borrow_flag INT,"
                     "return_flag INT)")
    mycursor.close()
    mydb.close()

def del_record_table():
    mydb =connect()
    mycursor = mydb.cursor()
    sql = "DROP TABLE IF EXISTS Record"
    mycursor.execute(sql)
    mycursor.close()
    mydb.close()
