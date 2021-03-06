#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import random

from database.user import UserDB
from database.record import RecordDB
from database.journal import JournalDB
from backstage.users import Reader
from backstage.users import JournalAdmin
from backstage.users import Admin
from backstage import config
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header


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
        results = JournalDB.get_info_by_dict("journal", {})
        len_info = len(results)
        for i in range(len_info):
            journal = dict()
            journal['name'] = results[i][4]
            journal['year'] = results[i][2]
            journal['stage'] = results[i][3]
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

        get_journal_dict = {

        }
        if name != "":
            get_journal_dict = {
                'name': name
            }
        results = JournalDB.get_info_by_dict("journal", get_journal_dict)
        len_info = len(results)
        for i in range(len_info):
            journal = dict()
            journal['name'] = results[i][4]
            journal['year'] = results[i][2]
            journal['stage'] = results[i][3]
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
        get_journal_info = {
            'name': name
        }
        if year != "":
            get_journal_info = {
                'name': name,
                'year': year
            }
            year = int(year)
        results = JournalDB.get_info_by_dict('journal', get_journal_info)
        for i in range(len(results)):
            journal_element = dict()
            journal_element['name'] = results[i][4]
            journal_element['year'] = results[i][2]
            journal_element['stage'] = results[i][3]
            journal_list.append(journal_element)
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
        results = JournalDB.get_journal_by_name_year_stage(name, year, stage)
        journal = dict()
        journal['name'] = name
        journal['year'] = year
        journal['stage'] = results[0][3]
        journal_list.append(journal)
        return data

    @classmethod
    def get_record_by_account(cls, account, status):
        """
        根据借书的用户名得到相应的数据
        :param account: 借书的用户名
        :return: data
        """
        if account == "":
            if status == '预约未借阅':
                get_record_info = {
                    'order_flag': 1,
                    'borrow_flag': 0,
                    'return_flag': 0
                }
            elif status == '借阅中':
                get_record_info = {
                    'borrow_flag': 1,
                    'return_flag': 0
                }
            else:
                get_record_info = {
                    'return_flag': 1
                }
        elif account != "":
            if status == '预约未借阅':
                get_record_info = {
                    'account': account,
                    'order_flag': 1,
                    'borrow_flag': 0,
                    'return_flag': 0
                }
            elif status == '借阅中':
                get_record_info = {
                    'account': account,
                    'borrow_flag': 1,
                    'return_flag': 0
                }
            else:
                get_record_info = {
                    'account': account,
                    'return_flag': 1
                }
        results = RecordDB.get_info_by_dict('record', get_record_info)
        record_list = []

        for i in range(len(results)):
            record_element = dict()
            key = (results[i][1])
            record_element['user_name'] = results[i][0]
            record_element['journal_name'] = JournalDB.get_name_by_key(key)
            record_element['journal_year'] = JournalDB.get_year_by_key(key)
            record_element['journal_stage'] = JournalDB.get_stage_by_key(key)
            record_element['status'] = status
            if status == '预约未借阅':
                record_element['time'] = results[i][2]
            elif status == '借阅中':
                record_element['time'] = results[i][3]
            else:
                record_element['time'] = results[i][4]

            record_list.append(record_element)
        data = {
            'record_list': record_list
        }

        return data

    @classmethod
    def get_record_by_journal_name(cls, journal_name, status):

        get_journal_info = {

        }
        if journal_name != "":
            get_journal_info = {
                'name': journal_name
            }
        journal_results = JournalDB.get_info_by_dict('journal', get_journal_info)
        record_list = []
        for i in range(len(journal_results)):
            record_element = dict()
            key = journal_results[i][0]
            get_record_info = {}
            if status == '预约未借阅':
                get_record_info = {
                    'key': key,
                    'order_flag': 1,
                    'borrow_flag': 0,
                    'return_flag': 0
                }
            elif status == '借阅中':
                get_record_info = {
                    'key': key,
                    'borrow_flag': 1,
                    'return_flag': 0
                }
            elif status == '归还':
                get_record_info = {
                    'key': key,
                    'return_flag': 1
                }
            record_results = RecordDB.get_info_by_dict('record', get_record_info)
            if len(record_results) == 0:
                continue
            else:
                for j in range(len(record_results)):
                    temp_key = record_results[j][1]
                    record_element['user_name'] = record_results[j][0]
                    record_element['journal_name'] = JournalDB.get_name_by_key(temp_key)
                    record_element['journal_year'] = JournalDB.get_year_by_key(temp_key)
                    record_element['journal_stage'] = JournalDB.get_stage_by_key(temp_key)
                    record_element['status'] = status
                    if status == '预约未借阅':
                        record_element['time'] = record_results[j][2]
                    elif status == '借阅中':
                        record_element['time'] = record_results[j][3]
                    else:
                        record_element['time'] = record_results[j][4]
                    record_list.append(record_element)
        data = {
            'record_list': record_list
        }
        return data

    @classmethod
    def get_object_by_account(cls, cur_account):
        user = object()
        if UserDB.get_user_identity(cur_account) == 'admin':
            user = Admin(cur_account)
        elif UserDB.get_user_identity(cur_account) == 'journal_admin':
            user = JournalAdmin(cur_account)
        elif UserDB.get_user_identity(cur_account):
            user = Reader(cur_account)
        return user

    @classmethod
    def line_chart_data(cls):
        def date_list(i):
            now_datetime = datetime.datetime.now()
            return str((now_datetime - datetime.timedelta(days=i)).month) + "月 " + str(
                (now_datetime - datetime.timedelta(days=i)).day) + "日"

        record_day = [date_list(6), date_list(5), date_list(4), date_list(3), date_list(2), date_list(1), date_list(0)]

        def get_a_date(i):
            now_datetime = datetime.datetime.now()
            delta_datetime = datetime.timedelta(days=i)
            return (now_datetime - delta_datetime).__format__('%Y%m%d')

        def num_list(choice: str):
            res = []
            for x in range(7):
                temp = RecordDB.get_this_day_record_num(get_a_date(x), choice)
                res.insert(0, temp)
            return res

        order_num = num_list('order')
        borrow_num = num_list('borrow')
        return_num = num_list('return')

        data = {
            'record_day': record_day,
            'order_num': order_num,
            'borrow_num': borrow_num,
            'return_num': return_num
        }

        return data

    @classmethod
    def validateEmail(cls, email_address):
        check_code = ""
        if len(email_address) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email_address) != None:
                sender = config.sender_email_address
                pwd = config.email_password
                receivers = email_address

                def get_check_code():
                    list1 = []
                    for i in range(6):

                        statu = random.randint(1, 3)
                        if statu == 1:  # 随机大写字母
                            a = random.randint(65, 90)
                            a_chr = chr(a)
                            list1.append(a_chr)
                        elif statu == 2:  # 随机小写字母
                            b = random.randint(97, 122)
                            b_chr = chr(b)
                            list1.append(b_chr)
                        elif statu == 3:  # 0-9的随机数
                            r = random.randint(0, 9)
                            list1.append(str(r))
                    ver_code = "".join(list1)
                    return ver_code

                check_code = get_check_code()
                message = MIMEText(check_code, 'plain', 'utf-8')
                message['Subject'] = '期刊借阅系统验证码'
                message['From'] = sender
                message['To'] = receivers
                smtp = smtplib.SMTP('smtp.163.com', port=25)
                smtp.login(sender, pwd)
                smtp.sendmail(sender, receivers, message.as_string())
                smtp.quit()
                flag = 1
        else:
            flag = 0
            check_code = '0'
        data = {
            'flag': flag,
            'check_code': check_code
        }
        return data

    @classmethod
    def confirm_email_account(cls, user_name, pwd1, pwd2, account, correct_check, input_check):
        if correct_check != input_check:
            flag = 0
            message = '验证码错误'
        else:
            if UserDB.check_user_exist(account) == True:
                flag = 0
                message = '当前邮箱账户已经存在'
            else:
                if pwd1 != pwd2:
                    flag = 0
                    message = '两次密码不符'
                else:
                    UserDB.add_user(account, pwd1, user_name, 'reader', 1)
                    flag = 1
                    message = '注册成功'
        data = {
            'flag': flag,
            'message': message
        }
        return data


if __name__ == '__main__':
    print()
    pass
