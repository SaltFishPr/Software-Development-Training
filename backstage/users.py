#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backstage.journals import Journal
from database.user import UserDB
from database.record import RecordDB
from database.journal import JournalDB
from backstage.records import Record


class User(object):
    def __init__(self, account):
        self._account = account
        self._identity = UserDB.get_user_identity(account)

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

    def get_journal_admin_info(self, choice):
        user_info = {
            'name': UserDB.get_user_name(self._account),
            'grade': UserDB.get_user_grade(self._account)
        }
        record_list = []
        journal_list = []

        for i, record_info in enumerate(RecordDB.get_info_by_dict('record', {})):
            record_element = dict()
            user_name = list(record_info)[0]
            key = list(record_info)[1]

            if list(record_info)[5] == 1 and list(record_info)[6] == 0 and list(record_info)[7] == 0:
                status = '预约未借阅'
            elif list(record_info)[6] == 1 and list(record_info)[7] == 0:
                status = '借阅中'
            elif list(record_info)[6] == 1 and list(record_info)[7] == 1:
                status = '已归还'
            else:
                status = '异常情况'
            order_time = list(record_info)[2]
            borrow_time = list(record_info)[3]
            return_time = list(record_info)[4]
            time = ""
            record_element['user_name'] = user_name
            record_element['status'] = status
            record_element['journal_name'] = JournalDB.get_name_by_key(key)
            record_element['journal_year'] = JournalDB.get_year_by_key(key)
            record_element['journal_stage'] = JournalDB.get_stage_by_key(key)
            if status == "预约未借阅":
                time = order_time
            elif status == "借阅中":
                time = borrow_time
            else:
                time = return_time
            record_element['time'] = time

            if choice == 'null':
                continue
            if choice == 'all':
                record_list.append(record_element)
                continue
            elif choice == 'order':
                if record_element['status'] == '预约未借阅':
                    record_list.append(record_element)
                continue
            elif choice == 'borrow':
                if record_element['status'] == '借阅中':
                    record_list.append(record_element)
                continue
            else:
                if record_element['status'] == '已归还':
                    record_list.append(record_element)
                continue

        for journal_info in JournalDB.get_info_by_dict('journal', {}):
            journal_element = dict()
            key = list(journal_info)[0]
            journal_element['journal_name'] = list(journal_info)[4]
            journal_element['journal_year'] = list(journal_info)[2]
            journal_element['journal_stage'] = list(journal_info)[3]
            journal_element['total_num'] = list(journal_info)[9]
            journal_element['lend_num'] = list(journal_info)[8]
            journal_element['order_num'] = list(journal_info)[7]
            journal_element['stock_num'] = list(journal_info)[6]
            journal_list.append(journal_element)
        data = {
            'record_list': record_list,
            'journal_list': journal_list,
            'user_info': user_info
        }

        return data

    def record_update(self, account, journal_name, journal_year, journal_stage, record_operation):
        """
        更新记录信息
        :param account: 读者账户
        :param journal_name: 期刊名
        :param journal_year: 期刊年份
        :param journal_stage: 期刊期数
        :param record_operation: 操作选择(处理预约、借阅、归还)
        :return: 操作结果(message)
        """
        journal_info = JournalDB.get_journal_by_name_year_stage(journal_name, journal_year, journal_stage)
        if not journal_info:
            data = {
                'flag': 0,
                'message': '没有这个期刊'
            }
            return data
        key = journal_info[0][0]
        if record_operation == '处理预约':
            get_record_dict = {
                'account': account,
                'key': key,
                'order_flag': 1,
                'borrow_flag': 0,
                'return_flag': 0
            }
            result = RecordDB.get_info_by_dict('record', get_record_dict)
            result.sort(key=lambda x: x[2])
            print(result)
            RecordDB.update_borrow_time(result[0][0], result[0][1], result[0][2])
            JournalDB.update_journal_num(key, journal_info[0][6] - 1, journal_info[0][7] - 1, journal_info[0][8] + 1,
                                         journal_info[0][9])
            message = '处理成功'
            flag = 1
        elif record_operation == '借阅':
            if journal_info[0][6] > journal_info[0][7]:
                RecordDB.add_borrow(account, key)
                JournalDB.update_journal_num(key, journal_info[0][6] - 1, journal_info[0][7], journal_info[0][8] + 1,
                                             journal_info[0][9])
                message = '借阅成功'
                flag = 1
            else:
                message = '借阅失败，库存不足'
                flag = 0
        elif record_operation == '归还':
            get_record_dict = {
                'account': account,
                'key': key,
                'borrow_flag': 1,
                'return_flag': 0
            }
            result = RecordDB.get_info_by_dict('record', get_record_dict)
            result.sort(key=lambda x: x[3])
            RecordDB.update_return_time(account, key, result[0][3])
            JournalDB.update_journal_num(key, journal_info[0][6] + 1, journal_info[0][7], journal_info[0][8] - 1,
                                         journal_info[0][9])
            message = '归还成功'
            flag = 1
        data = {
            'flag': flag,
            'message': message
        }
        return data

    def journal_total_num_update(self, journal_name, journal_year, journal_stage, update_method, num):
        journal_info = JournalDB.get_journal_by_name_year_stage(journal_name, journal_year, journal_stage)
        key = journal_info[0][0]
        if update_method == '库存增加':
            JournalDB.update_journal_num(key, journal_info[0][6] + num, journal_info[0][7], journal_info[0][8],
                                         journal_info[0][9] + num)
            flag = 1
            message = '成功'
        elif update_method == '库存减少':
            if num <= journal_info[0][6]:
                JournalDB.update_journal_num(key, journal_info[0][6] - num, journal_info[0][7], journal_info[0][8],
                                             journal_info[0][9] - num)
                flag = 1
                message = '成功'
            else:
                flag = 0
                message = '库存不足'
        else:
            flag = 0
        data = {
            'flag': flag,
            'message': message
        }
        return data


class Reader(User):
    def __init__(self, account):
        super(Reader, self).__init__(account)

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
            results = RecordDB.get_record_by_account(self._account)[i]
            if results[5] == 1 and results[6] == 0 and results[7] == 0:
                borrow['status'] = '预约未借阅'
            elif results[6] == 1 and results[7] == 0:
                borrow['status'] = '借阅中'
            elif results[6] == 1 and results[7] == 1:
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
    def order(self, journal_name, journal_year, journal_stage):
        """

        :param journal_name:
        :param journal_year:
        :param journal_stage:
        :return:
        """
        journal_info = JournalDB.get_journal_by_name_year_stage(journal_name, journal_year, journal_stage)
        key = journal_info[0][0]

        # 库存数大于预约数 可以预约
        if journal_info[0][6] > journal_info[0][7]:
            RecordDB.add_order(self._account, key)
            JournalDB.update_journal_num(key,journal_info[0][6],journal_info[0][7]+1,journal_info[0][8],journal_info[0][9])
            flag = 1
            message = '预约成功，请到书库借阅!'
        else:
            flag = 0
            message = '您预约的期刊已经没有库存了！'

        data = {
            'flag': flag,
            'message': message
        }
        return data

if __name__ == '__main__':
    user_obj = JournalAdmin('wws')
    print(user_obj.record_update('badwoman', 'science', 1999, 1, '归还'))
