from database.record import RecordDB


class Record(object):
    def __init__(self):
        pass

    @classmethod
    def get_record_status(cls, key):
        """
        根据key得到当前的用户借阅状态
        :param key:
        :return:
        """
        get_record_dict = {
            'key': key
        }
        results = RecordDB.get_info_by_dict('record', get_record_dict)
        if len(results) == 0:
            status = '异常情况'
            return
        if results[0][5] == 1 and results[0][6] == 0 and results[0][7] == 0:
            status = '预约未借阅'
        elif results[0][6] == 1 and results[0][7] == 0:
            status = '借阅中'
        elif results[0][6] == 1 and results[0][7] == 1:
            status = '已归还'
        else:
            status = '异常情况'
        return status


if __name__ == '__main__':
    print(Record.get_record_status(1))
