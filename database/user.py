from database.db_base import DBBase


class UserDB(DBBase):
    @classmethod
    def check_user_exist(cls, account):
        """
        新建账户时检测账户是否已经存在
        :param account: 用户账户
        :return: bool
        """
        sql = "SELECT * FROM user WHERE account  = '%s'" % account
        results = cls._execute_sql(UserDB(), sql, 'select')
        if not results:
            return False
        else:
            return True

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
        sql = "INSERT INTO user (account,password,name,identity,grade) VALUES ('%s','%s','%s','%s','%s')" % (
            account, password, username, identity, grade)
        cls._execute_sql(UserDB(), sql, 'insert')

    @classmethod
    def check_account(cls, account, password):
        """
        检测账户是否存在，返回账户信息
        :param account: 账号
        :param password: 密码
        :return: 账户所有信息的一个list
        """
        sql = "SELECT * FROM user WHERE account  = '%s' AND password = '%s'" % (account, password)
        result = cls._execute_sql(UserDB(), sql, 'select')
        if len(result) == 0:
            return None
        else:
            return list(result[0])

    @classmethod
    def remove_user(cls, account):
        """
        根据账户注销用户
        :param account:账户
        :return:
        """
        sql = "DELETE FROM user WHERE account = '%s'" % account
        cls._execute_sql(UserDB(), sql, 'delete')

    @classmethod
    def update_user_password(cls, account, new_password):
        """
        根据账户名更新密码
        :param account:账户
        :param new_password:新密码
        :return:
        """
        sql = "UPDATE user SET password='%s' WHERE account = '%s'" % (new_password, account)
        cls._execute_sql(UserDB(), sql, 'update')

    @classmethod
    def update_user_name(cls, account, new_name):
        """
        根据账户名更新用户昵称
        :param account:账户
        :param new_name:新昵称
        :return:
        """
        sql = "UPDATE user SET name='%s' WHERE account = '%s'" % (new_name, account)
        cls._execute_sql(UserDB(), sql, 'update')

    @classmethod
    def update_user_identity(cls, account, new_identity):
        """
        更新用户的身份
        :param account:账户
        :param new_identity:新身份
        :return:
        """
        sql = "UPDATE user SET identity='%s' WHERE account ='%s'" % (new_identity, account)
        cls._execute_sql(UserDB(), sql, 'update')

    @classmethod
    def update_user_grade(cls, account, new_grade):
        """
        更新用户的等级
        :param account:账户
        :param new_grade:新等级
        :return:
        """
        sql = "UPDATE user SET grade='%s' WHERE account = '%s'" % (new_grade, account)
        cls._execute_sql(UserDB(), sql, 'update')

    @classmethod
    def get_user_password(cls, account):
        """

        :param account: 用户账户
        :return: 用户密码
        """
        sql = "SELECT password FROM user WHERE account  = '%s'" % account
        results = cls._execute_sql(UserDB(), sql, 'select')
        password = results[0][0]
        return password

    @classmethod
    def get_user_name(cls, account):
        """
        得到用户的昵称
        :param account:账户
        :return:
        """
        sql = "SELECT name FROM user WHERE account  = '%s'" % account
        results = cls._execute_sql(UserDB(), sql, 'select')
        name = results[0][0]
        return name

    @classmethod
    def get_user_identity(cls, account):
        """
        得到用户的身份
        :param account:账户
        :return:
        """
        sql = "SELECT identity FROM user WHERE account  = '%s'" % account
        results = cls._execute_sql(UserDB(), sql, 'select')
        identity = results[0][0]
        return identity

    @classmethod
    def get_user_grade(cls, account):
        """
        得到用户的等级
        :param account:账户
        :return:
        """
        sql = "SELECT grade FROM user WHERE account  = '%s'" % account
        results = cls._execute_sql(UserDB(), sql, 'select')
        grade = results[0][0]
        return grade

    @classmethod
    def get_info_by_identity(cls, identity):
        sql = "SELECT * FROM user WHERE identity  = '%s'" % identity
        results = cls._execute_sql(UserDB(), sql, 'select')
        return results


if __name__ == '__main__':
    # dict_test = {
    #     'grade': 1
    # }
    # UserDB.get_user_info('user', dict_test)
    print(UserDB.check_user_exist('badwoman'))
    # print(UserDB.check_user_exist('jl'))
