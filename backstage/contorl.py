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
                6] == 0 and RecordDB.get_record_by_account(account)[i][7] == 0:
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
    def push_borrow_info(cls, account):
        """
        给前端需要的借阅中心信息
        :param account: 用户账户
        :return: data
        """
        user = {
            'name': UserDB.get_user_name(account),
            'grade': UserDB.get_user_grade(account)
        }
        data = {
            'user_info': user
        }
        return data

    @classmethod
    def push_user_info_data(cls, account):
        """
        把数据提交给user_data_page
        :param account: 用户账号
        :return: data
        """
        user = {
            'name': UserDB.get_user_name(account),
            'grade': UserDB.get_user_grade(account),
            'account': account
        }
        data = {
            'user_info': user
        }
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
    def modify_user_info(cls, account, name, grade, identity):
        """
        系统管理员修改用户的信息
        :param account: 所修改的用户名
        :param name: 修改后的名字
        :param grade: 修改后的等级
        :param identity: 修改后的权限
        :return: data
        """
        name_flag = 0
        grade_flag = 0
        identity_flag = 0
        if UserDB.check_user_exist(account) == False:
            print("帐号错误")
            data = {
                'flag': 0
            }
            return data
        print("准备name检测")
        if name != "" and name != UserDB.get_user_name(account):
            UserDB.update_user_name(account, name)
            name_flag = 1
            print("name 成功")
        print("准备grade检测")
        if grade != "" and grade != UserDB.get_user_grade(account):
            UserDB.update_user_grade(account, grade)
            grade_flag = 1
            print("grade 成功")
        print("准备identity检测")
        if identity != "" and identity != UserDB.get_user_identity(account):
            UserDB.update_user_identity(account, identity)
            identity_flag = 1
            print("identity 成功")
        if name_flag + grade_flag + identity_flag == 0:
            print("修改错误")
            data = {
                'flag': 0
            }
            return data
        else:
            data = {
                'flag': 1
            }
            print("输出一下data")
            print(data)
            return data

    @classmethod
    def get_user_info(cls):
        """
        管理员得到(读者)和(期刊管理员)的信息
        :return:data
        """
        reader_list = []
        journal_admin_list = []

        reader_results = UserDB.get_info_by_identity('reader')
        journal_admin_results = UserDB.get_info_by_identity('journal_admin')
        for i in range(len(reader_results)):
            reader = dict()
            reader['account'] = reader_results[i][0]
            reader['name'] = reader_results[i][2]
            reader['grade'] = reader_results[i][4]
            reader_list.append(reader)
        for i in range(len(journal_admin_results)):
            journal_admin = dict()
            journal_admin['account'] = journal_admin_results[i][0]
            journal_admin['name'] = journal_admin_results[i][2]
            journal_admin['grade'] = journal_admin_results[i][4]
            journal_admin_list.append(journal_admin)
        data = {
            'reader_list': reader_list,
            'journal_admin_list': journal_admin_list,
        }
        return data

    @classmethod
    def get_all_user_info(cls):
        """
        管理员得到全部的用户信息进行修改操作
        :return: data
        """
        account_list = []
        data = {
            'account_list': account_list
        }

        get_user_dict = {

        }
        user_results = UserDB.get_info_by_dict('User', get_user_dict)
        for i in range(len(user_results)):
            user_account = dict()
            user_account['account'] = user_results[i][0]
            account_list.append(user_account)
        return data


if __name__ == '__main__':
    print(JsonPack.get_all_user_info())
