from database import db_init


# 注册用户
def add_user(account, password, username, identity, grade):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "INSERT INTO user (account,password,name,identity,grade) VALUES ('%s','%s','%s','%s','%s')" % (
        account, password, username, identity, grade)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


# 检测账户是否存在
def check_account_exsit(account):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "SELECT * FROM user WHERE account  = '%s'" % (account)
    mycursor.execute(sql)
    values = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    if len(values) == 0:
        return False
    else:
        return True


# 根据账户检测密码是否正确
def check_password_exsit(account):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "SELECT password FROM user WHERE account  = '%s'" % (account)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    for row in results:
        pwd = row[0]
    mycursor.close()
    mydb.close()
    return pwd


# 根据账户注销用户
def del_user(account):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "DELETE FROM user WHERE account = '%s'" % (account)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


# 根据账户名更新密码
def update_user_password(account, newpwd):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "UPDATE user SET password='%s' WHERE account = '%s'" % (newpwd, account)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


# 根据账户名更新用户名
def update_user_name(account, newname):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "UPDATE user SET name='%s' WHERE account = '%s'" % (newname, account)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


# 更新用户的身份
def update_user_identity(account, newidentity):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "UPDATE user SET identity='%s' WHERE account ='%s'" % (newidentity, account)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


# 更新用户的等级
def update_user_grade(account, newgrade):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "UPDATE user SET grade='%s' WHERE account = '%s'" % (newgrade, account)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


# 得到账户的名字
def ask_user_name(account):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "SELECT name FROM user WHERE account  = '%s'" % (account)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    for row in results:
        name = row[0]
    mycursor.close()
    mydb.close()
    return name


# 得到用户的权限
def ask_user_identity(account):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "SELECT identity FROM user WHERE account  = '%s'" % (account)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    for row in results:
        identity = row[0]
    mycursor.close()
    mydb.close()
    return identity


# 得到读者用户的等级
def ask_user_grade(account):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "SELECT grade FROM user WHERE account  = '%s'" % (account)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    for row in results:
        grade = row[0]
    mycursor.close()
    mydb.close()
    return grade

#得到用户的名字
def get_name_by_account(account):
    mydb = db_init.connect()
    mycursor = mydb.cursor()
    sql = "SELECT name FROM USer WHERE account  = '%s'" % (account)
    mycursor.execute(sql)
    results = mycursor.fetchall()
    for row in results:
        name = row[0]
    mycursor.close()
    mydb.close()
    return name

if __name__ == '__main__':
    print(get_name_by_account('jl'))