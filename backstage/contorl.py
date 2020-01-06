#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from database.user import UserDB
from database.record import RecordDB
from database.journal import JournalDB


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
        if (UserDB.check_user_exist(account)):  # 如果存在相同的账户
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
        if (UserDB.check_account(account, pwd) == False):
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
    def get_reader_center_info(cls, account):
        """
        返回读者当前的借阅期刊情况
        :param account: 当前账户
        :return: data
        """
        name = UserDB.get_user_name(account)
        grarde = UserDB.get_user_grade(account)
        user_info = {
            'name': name,
            'grade': grarde
        }
        borrow_list = []
        borrow = {
            'name': "",
            'status': "",
            'time_1': "",
            'time_2': ""
        }
        info_len = RecordDB.get_info_length(account)
        key_list = RecordDB.get_key_by_account(account)
        for i in range(info_len):
            borrow = dict()
            borrow['name'] = JournalDB.get_name_by_key(key_list[i])
            # 1 0 0预约未借阅
            # x 1 0  借阅 未归还
            # x 1 1 归还
            if RecordDB.get_record_by_account(account)[i][5] == 1 and RecordDB.get_record_by_account(account)[i][
                6] == 0 and \
                    RecordDB.get_record_by_account(account)[i][7] == 0:
                borrow['status'] = '预约未借阅'
            elif RecordDB.get_record_by_account(account)[i][6] == 1 and RecordDB.get_record_by_account(account)[i][
                7] == 0:
                borrow['status'] = '借阅中'
            elif RecordDB.get_record_by_account(account)[i][6] == 1 and RecordDB.get_record_by_account(account)[i][
                7] == 1:
                borrow['status'] = '已归还'
            else:
                borrow['status'] = '异常情况'
            if borrow['status'] == '预约未借阅':
                borrow['time_1'] = '未借阅'
                borrow['time_2'] = '未借阅'
            elif borrow['status'] == '借阅中':
                borrow['time_1'] = RecordDB.get_record_by_account(account)[i][3]
                borrow['time_2'] = '未归还'
            elif borrow['status'] == '已归还':
                borrow['time_1'] = RecordDB.get_record_by_account(account)[i][3]
                borrow['time_2'] = RecordDB.get_record_by_account(account)[i][4]
            else:
                borrow['time_1'] = '异常情况'
                borrow['time_2'] = '异常情况'
            borrow_list.append(borrow)
        data = {
            'user_info': user_info,
            'borrow_list': borrow_list
        }
        return data

    @classmethod
    def update_user_check(cls, account, name, pwd):
        """
        判断更新用户信息是否成功
        :param account: 当前账户
        :param name: 更新名字
        :param pwd: 更新密码
        :return: data
        """
        dict1 = {
            'flag': -1
        }
        data = {
            'dict': dict1
        }
        if name == "":
            if pwd == UserDB.get_user_password(account):
                dict1['flag'] = 0
            else:
                UserDB.update_user_password(account, pwd)
                dict1['flag'] = 1
        elif pwd == "":
            if name == UserDB.get_user_name(account):
                dict1['flag'] = 0
            else:
                UserDB.update_user_name(account, name)
                dict1['flag'] = 1
        else:
            if name == UserDB.get_user_name(account):
                if pwd == UserDB.get_user_password(account):
                    dict1['flag'] = 0
                else:
                    UserDB.update_user_password(account, pwd)
                    dict1['flag'] = 1
            else:
                if pwd == UserDB.get_user_password(account):
                    UserDB.update_user_name(account, name)
                    dict1['flag'] = 1
                else:
                    UserDB.update_user_password(account, pwd)
                    UserDB.update_user_name(account, name)
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
    def get_journal_stage(clf, name, year):
        """
        根据期刊的名字和年得到期刊的所有期
        :param name:
        :param year:
        :return:
        """
        journal_list = []
        data = {
            'journal_list': journal_list
        }
        results = JournalDB.get_stage_by_nameandyear(name, year)
        for temp in results:
            journal = dict()
            journal['name'] = name
            journal['year'] = year
            journal['stage'] = temp
            journal_list.append(journal)
        return data

    @classmethod
    def config_journal(clf,name,year,stage):
        """

        :param name:
        :param year:
        :param stage:
        :return:
        """

if __name__ == '__main__':
    print(JsonPack.get_journal_year('science'))
