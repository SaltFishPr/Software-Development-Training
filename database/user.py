from database.db_base import DBBase


class UserDB(DBBase):
    @classmethod
    def check_user_exist(cls, account):
        """
        新建账户时检测账户是否已经存在
        :param account: 用户账户
        :return: bool
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM user WHERE account  = '%s'" % account
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if not results:
            return False
        else:
            return True
        pass

    @classmethod
    def add_user(cls, account, password, username, identity, grade):
        """
        注册用户
        :param account:账户
        :param password:密码
        :param username:昵称
        :param identity:身份
        :param grade:等级
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "INSERT INTO user (account,password,name,identity,grade) VALUES ('%s','%s','%s','%s','%s')" % (
            account, password, username, identity, grade)
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()

    @classmethod
    def check_account(cls, account, password):
        """
        检测账户是否存在，返回账户信息
        :param account: 账号
        :param password: 密码
        :return: 账户所有信息的一个list
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM user WHERE account  = '%s' AND password = '%s'" % (account, password)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) == 0:
            return None
        else:
            return list(result[0])

    @classmethod
    def del_user(cls, account):
        """
        根据账户注销用户
        :param account:账户
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "DELETE FROM user WHERE account = '%s'" % (account)
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()

    @classmethod
    def update_user_password(cls, account, new_password):
        """
        根据账户名更新密码
        :param account:账户
        :param new_password:新密码
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "UPDATE user SET password='%s' WHERE account = '%s'" % (new_password, account)
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()

    @classmethod
    def update_user_name(cls, account, new_name):
        """
        根据账户名更新用户昵称
        :param account:账户
        :param new_name:新昵称
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "UPDATE user SET name='%s' WHERE account = '%s'" % (new_name, account)
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()

    @classmethod
    def update_user_identity(cls, account, new_identity):
        """
        更新用户的身份
        :param account:账户
        :param new_identity:新身份
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "UPDATE user SET identity='%s' WHERE account ='%s'" % (new_identity, account)
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()

    @classmethod
    def update_user_grade(cls, account, new_grade):
        """
        更新用户的等级
        :param account:账户
        :param new_grade:新等级
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "UPDATE user SET grade='%s' WHERE account = '%s'" % (new_grade, account)
        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()

    @classmethod
    def get_user_password(cls, account):
        """

        :param account: 用户账户
        :return: 用户密码
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT password FROM user WHERE account  = '%s'" % account
        mycursor.execute(sql)
        results = mycursor.fetchall()
        password = results[0][0]
        mycursor.close()
        mydb.close()
        return password

    @classmethod
    def get_user_name(cls, account):
        """
        得到用户的昵称
        :param account:账户
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT name FROM user WHERE account  = '%s'" % account
        mycursor.execute(sql)
        results = mycursor.fetchall()
        name = results[0][0]
        mycursor.close()
        mydb.close()
        return name

    @classmethod
    def get_user_identity(cls, account):
        """
        得到用户的身份
        :param account:账户
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT identity FROM user WHERE account  = '%s'" % account
        mycursor.execute(sql)
        results = mycursor.fetchall()
        identity = results[0][0]
        mycursor.close()
        mydb.close()
        return identity

    @classmethod
    def get_user_grade(cls, account):
        """
        得到用户的等级
        :param account:账户
        :return:
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT grade FROM user WHERE account  = '%s'" % account
        mycursor.execute(sql)
        results = mycursor.fetchall()
        grade = results[0][0]
        mycursor.close()
        mydb.close()
        return grade

    @classmethod
    def get_name_by_account(cls, account):
        """
        得到用户的昵称
        :param account: 用户账户
        :return: 用户昵称
        """
        mydb = DBBase.connect()
        mycursor = mydb.cursor()
        sql = "SELECT name FROM USer WHERE account  = '%s'" % account
        mycursor.execute(sql)
        results = mycursor.fetchall()
        name = results[0][0]
        mycursor.close()
        mydb.close()
        return name


if __name__ == '__main__':
    print(UserDB.check_user_exist('jl'))
