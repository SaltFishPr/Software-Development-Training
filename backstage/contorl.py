#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from database.user import UserDB
from database.record import RecordDB
from database.journal import JournalDB
from backstage.users import User
from backstage.users import Reader
from backstage.users import JournalAdmin
from backstage.users import Admin


class JsonPack(object):
    @classmethod
    def register_check(cls, account, pwd, name, identity, grade):
        """
        注册账户的时候判断是否注册成功
        :param account: 注册账户名
        :param pwd: 密码
        :param name: 名字
        :param identity: 权限（reader）
        :param grade: 等级（1）
        :return: data
        """
        dict1 = {
            'flag': -1
        }
        data = {
            'dict': dict1
        }
        # 执行数据库的插入操作
        if UserDB.check_user_exist(account):  # 如果存在相同的账户
            dict1['flag'] = 0
        else:
            UserDB.add_user(account, pwd, name, identity, grade)
            dict1['flag'] = 1
        return data

    @classmethod
    def login_check(cls, account, pwd):
        """
        登录判断密码是否正确以及登录时的身份
        :param account: 登录账户检测
        :param pwd: 登录密码检测
        :return: data
        """
        dict1 = {
            'flag': -1
        }
        data = {
            'dict': dict1,
            'pageTitle': 8798,
            'pageData': 66
        }
        if not UserDB.check_account(account, pwd):
            dict1['flag'] = -1
        else:
            if UserDB.get_user_identity(account) == 'admin':
                dict1['flag'] = 2
            elif UserDB.get_user_identity(account) == 'journal_admin':
                dict1['flag'] = 3
            else:
                dict1['flag'] = 1
        return data

    @classmethod
    def get_journal_info(cls):
        """
        返回所有的期刊数据，只取名字
        :return:data
        """
        journal_list = []
        data = {
            'journal_list': journal_list
        }
        journal = {
            'name': "",
            'year': "null",
            'stage': "null"
        }
        results = JournalDB.get_journal()
        len_info = len(JournalDB.get_journal())
        for i in range(len_info):
            journal = dict()
            journal['name'] = results[i][4]
            journal['year'] = "null"
            journal['stage'] = "null"
            journal_list.append(journal)
        return data

    @classmethod
    def get_journal_year(cls, name):
        """
        根据期刊的名字得到期刊的年
        :param name:
        :return:data
        """
        journal_list = []
        data = {
            'journal_list': journal_list
        }

        results = JournalDB.get_year_by_name(name)
        for temp in results:
            journal = dict()
            journal['name'] = 'science'
            journal['year'] = temp
            journal['stage'] = 'null'
            journal_list.append(journal)
        return data

    @classmethod
    def get_journal_stage(cls, name, year):
        """
        根据期刊的名字和年得到期刊的所有期
        :param name:
        :param year:
        :return:data
        """
        journal_list = []
        data = {
            'journal_list': journal_list
        }
        results = JournalDB.get_stage_by_name_and_year(name, year)
        for temp in results:
            journal = dict()
            journal['name'] = name
            journal['year'] = year
            journal['stage'] = temp
            journal_list.append(journal)
        return data

    @classmethod
    def confirm_journal(cls, name, year, stage):
        """
        根据三个参数得到一个确定的期刊
        :param name:期刊名字
        :param year:期刊的发行年限
        :param stage:发行年限下的期号
        :return:data
        """
        journal_list = []
        data = {
            'journal_list': journal_list
        }
        results = JournalDB.get_journal_by_stage(name, year, stage)
        journal = dict()
        journal['name'] = name
        journal['year'] = year
        journal['stage'] = results[0][3]
        journal_list.append(journal)
        return data

    @classmethod
    def put_admin_info(cls, account):
        """
        把数据提交给登录的系统 管理员
        :param account: 系统管理员的账户
        :return: data
        """
        user_info = {
            'name': UserDB.get_user_name(account),
            'grade': UserDB.get_user_grade(account)
        }
        data = {
            'user_info': user_info
        }
        return data

    @classmethod
    def get_object_by_account(cls, cur_account):
        if UserDB.get_user_identity(cur_account) == 'reader':
            reader = Reader(cur_account)
            return reader
        elif UserDB.get_user_identity(cur_account) == 'admin':
            admin = Admin(cur_account)
            return admin
        else:
            journal_admin = JournalAdmin(cur_account)
            return journal_admin


if __name__ == '__main__':
    print(JsonPack.get_all_user_info())
