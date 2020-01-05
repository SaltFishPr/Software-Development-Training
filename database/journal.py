from database import db_init


def get_name_by_key(key):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "SELECT name FROM journal WHERE key = '%d' " % (key)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    for row in results:
        name = row[0]
    mycursor.close()
    mydb.close()
    return name


if __name__ == '__main__':
    print(get_name_by_key(1))