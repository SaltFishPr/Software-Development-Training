#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from database.record import RecordDB
from database.journal import JournalDB

class Journal(object):
    def __init__(self, main_key, issn, year, stage, name, tags, stock_num, order_num, lend_num, total_num, press,
                 editor):
        """
        创建期刊
        :param main_key: 主键，唯一
        :param issn: ISSN号(char)
        :param year: 年(char)
        :param stage: 期(char)
        :param name: 期刊名(char)
        :param tags: 标签(list)
        :param stock_num:库存数量(int)
        :param order_num: 预约数量(int)
        :param lend_num: 借出数量(int)
        :param total_num: 总数(int)
        :param press: 出版社(char)
        :param editor: 编辑(char)
        """
        self.__main_key = main_key
        self.__issn = issn
        self.__year = year
        self.__stage = stage
        self.__name = name
        self.__tags = tags
        self.__stock_num = stock_num
        self.__order_num = order_num
        self.__lend_num = lend_num
        self.__total_num = total_num
        self.__press = press
        self.__editor = editor
        pass



if __name__ == '__main__':
    pass
