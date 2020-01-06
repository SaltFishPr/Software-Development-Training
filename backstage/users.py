#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backstage.journals import Journal


class User(object):
    def __init__(self, account, password, name):
        self._account = account
        self._password = password
        self._name = name

    def get_account(self):
        return self._account

    def get_password(self):
        return self._password

    def get_name(self):
        return self._name


class Admin(User):
    def __init__(self, account, password, name):
        super(Admin, self).__init__(account, password, name)
        self.__identity = "admin"

    # 冻结账户
    def _freeze_account(self):
        pass

    # 删除用户
    def _remove_account(self):
        pass


class PeriodicalAdmin(User):
    def __init__(self, account, password, name):
        super(PeriodicalAdmin, self).__init__(account, password, name)
        self.__identity = "periodical_admin"

    # 增加新的期刊
    def _add_journal(self, journal: Journal):
        # TODO:调用数据库insert
        pass

    # 删除某一期的期刊
    def _remove_journal(self, journal_issn, journal_year, journal_stage):
        # TODO:调用数据库drop
        pass

    # 增加或减少期刊数量
    def _update_journal(self, journal_issn, journal_year, journal_stage):
        # TODO:调用数据库update
        pass

    # 借阅
    def _borrow_journal(self):
        pass

    # 归还
    def _return_journal(self):
        pass


class Reader(User):
    def __init__(self, account, password, name, grade):
        super(Reader, self).__init__(account, password, name)
        self.__identity = "reader"
        self.__grade = grade

    def _update_user_name(self, name):
        self._name = name
        # TODO:调用数据库update

    def _update_user_password(self, password):
        self._password = password
        # TODO:调用数据库update

    def get_self_info(self):
        """
        返回个人信息，供查询个人信息调用
        :return:list
        """
        return [self._name, self.__grade]

    def _query_borrow_info(self):
        """
        查询个人借阅信息
        :return:
        """
        # TODO:调用数据库查询
        return

    # 预约
    def _order(self):
        pass


if __name__ == '__main__':
    print("test")
    reader = User("aaa", "12300", "xd")
