#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backstage.journals import Journal
from database.user import UserDB
from database.record import RecordDB
from database.journal import JournalDB
from backstage.record import Record

class User(object):
    def __init__(self, account):
        self._account = account
        self._identity = 'reader'

    def get_identity(self):
        """
        得到用户的身份
        :return:
        """
        return self._identity

    def get_self_info(self, choice):
        """
        根据choice得到本账户的信息
        :param choice: 要得到哪些信息的选项
        :return:
        """
        user = {

        }
        data = {
            'user_info': user
        }
        get_user_dict = {
            'account': self._account
        }
        user_info_results = UserDB.get_info_by_dict('User', get_user_dict)
        if choice == 'account_name_grade':
            user['account'] = user_info_results[0][0]
            user['name'] = user_info_results[0][2]
            user['grade'] = user_info_results[0][4]
        elif choice == 'name_grade':
            user['name'] = user_info_results[0][2]
            user['grade'] = user_info_results[0][4]

        return data

    def check_info_update(self, account, name, pwd):
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


class Admin(User):
    def __init__(self, account):
        super(Admin, self).__init__(account)
        self._identity = "admin"

    def get_all_user_info(self):
        """
        管理员得到所有用户的信息
        :return: data(dict)
        """
        account_list = []
        data = {
            'account_list': account_list
        }

        get_user_dict = {

        }
        user_info_results = UserDB.get_info_by_dict('User', get_user_dict)
        for i in range(len(user_info_results)):
            user_account = dict()
            user_account['account'] = user_info_results[i][0]
            account_list.append(user_account)
        return data

    def remove_account(self, account):
        dict1 = {
            'flag': -1
        }
        data = {
            'dict': dict1
        }
        # 执行数据库的删除操作
        if UserDB.check_user_exist(account):  # 如果存在该用户
            UserDB.remove_user(account)
            dict1['flag'] = 1
        else:  # 用户不存在
            dict1['flag'] = 0
        return data

    def get_data_by_account(self, account):
        """
        通过用户账户得到 相应信息 给 管理员用
        :param account: 用户账户
        :return: data
        """
        data = {

        }
        get_user_dict = {
            'account': account
        }
        user_info_results = UserDB.get_info_by_dict('User', get_user_dict)
        data['name'] = user_info_results[0][2]
        data['grade'] = user_info_results[0][4]
        data['identity'] = user_info_results[0][3]

        return data

    def get_user_info_group_by_identity(self):
        """
        管理员得到(读者)和(期刊管理员)的信息
        :return:data
        """
        reader_list = []
        journal_admin_list = []

        get_user_dict = {
            'identity': 'reader'
        }
        for user_info in UserDB.get_info_by_dict('User', get_user_dict):
            reader_list.append({'account': list(user_info)[0],
                                'name': list(user_info)[2],
                                'grade': list(user_info)[4]})
        get_user_dict = {
            'identity': 'journal_admin'
        }
        for user_info in UserDB.get_info_by_dict('User', get_user_dict):
            journal_admin_list.append({'account': list(user_info)[0],
                                       'name': list(user_info)[2],
                                       'grade': list(user_info)[4]})
        data = {
            'reader_list': reader_list,
            'journal_admin_list': journal_admin_list,
        }
        return data

    def modify_user_info(self, account, name, grade, identity):
        """
        系统管理员修改用户的信息
        :param account: 所修改的用户名
        :param name: 修改后的名字
        :param grade: 修改后的等级
        :param identity: 修改后的权限
        :return: data
        """
        name_flag = False
        grade_flag = False
        identity_flag = False
        if not UserDB.check_user_exist(account):
            data = {
                'flag': 0
            }
            return data
        if name != "" and name != UserDB.get_user_name(account):
            UserDB.update_user_name(account, name)
            name_flag = 1
        if grade != "" and grade != UserDB.get_user_grade(account):
            UserDB.update_user_grade(account, grade)
            grade_flag = 1
        if identity != "" and identity != UserDB.get_user_identity(account):
            UserDB.update_user_identity(account, identity)
            identity_flag = 1
        if name_flag or grade_flag or identity_flag:
            data = {
                'flag': 1
            }
            return data
        else:
            data = {
                'flag': 0
            }
            return data

    # 冻结账户
    def _freeze_account(self):
        pass


class JournalAdmin(User):
    def __init__(self, account):
        super(JournalAdmin, self).__init__(account)
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
    def __init__(self, account):
        super(Reader, self).__init__(account)
        self.__identity = "reader"

    def _update_user_name(self, name):
        self._name = name
        # TODO:调用数据库update

    def _update_user_password(self, password):
        self._password = password
        # TODO:调用数据库update

    def get_record_info(self):
        """
        返回读者当前的借阅期刊情况
        :return: data
        """
        name = UserDB.get_user_name(self._account)
        grarde = UserDB.get_user_grade(self._account)
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
        info_len = RecordDB.get_info_length(self._account)
        key_list = RecordDB.get_key_by_account(self._account)
        for i in range(info_len):
            borrow = dict()
            borrow['name'] = JournalDB.get_name_by_key(key_list[i])
            # 1 0 0预约未借阅
            # x 1 0  借阅 未归还
            # x 1 1 归还
            if RecordDB.get_record_by_account(self._account)[i][5] == 1 and \
                    RecordDB.get_record_by_account(self._account)[i][
                        6] == 0 and RecordDB.get_record_by_account(self._account)[i][7] == 0:
                borrow['status'] = '预约未借阅'
            elif RecordDB.get_record_by_account(self._account)[i][6] == 1 and \
                    RecordDB.get_record_by_account(self._account)[i][
                        7] == 0:
                borrow['status'] = '借阅中'
            elif RecordDB.get_record_by_account(self._account)[i][6] == 1 and \
                    RecordDB.get_record_by_account(self._account)[i][
                        7] == 1:
                borrow['status'] = '已归还'
            else:
                borrow['status'] = '异常情况'
            if borrow['status'] == '预约未借阅':
                borrow['time_1'] = '未借阅'
                borrow['time_2'] = '未借阅'
            elif borrow['status'] == '借阅中':
                borrow['time_1'] = RecordDB.get_record_by_account(self._account)[i][3]
                borrow['time_2'] = '未归还'
            elif borrow['status'] == '已归还':
                borrow['time_1'] = RecordDB.get_record_by_account(self._account)[i][3]
                borrow['time_2'] = RecordDB.get_record_by_account(self._account)[i][4]
            else:
                borrow['time_1'] = '异常情况'
                borrow['time_2'] = '异常情况'
            borrow_list.append(borrow)
        data = {
            'user_info': user_info,
            'borrow_list': borrow_list
        }
        return data

    # 预约
    def _order(self):
        pass


if __name__ == '__main__':
    user_obj = Admin('jl')
    print(user_obj.remove_account('test1'))
