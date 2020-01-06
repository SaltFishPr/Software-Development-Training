from database import user
from database import record
from database import journal

print(record.ask_record_by_account('jl'))
key_list = record.ask_key_by_account('jl')
print(key_list)

info_len = record.get_info_account('jl')
borrow_list = []
borrow = {
    'name': "",
    'status': "",
    'time_1': "",
    'time_2': ""
}
for i in range(info_len):
    borrow = dict()
    borrow['name'] = journal.get_name_by_key(key_list[i])
    # 1 0 0预约未借阅
    # x 1 0  借阅 未归还
    # x 1 1 归还
    if record.ask_record_by_account('jl')[i][5] == 1 and record.ask_record_by_account('jl')[i][6] == 0 and \
            record.ask_record_by_account('jl')[i][7] == 0:
        borrow['status'] = '预约未借阅'
    elif record.ask_record_by_account('jl')[i][6] == 1 and record.ask_record_by_account('jl')[i][7] == 0:
        borrow['status'] = '借阅中'
    elif record.ask_record_by_account('jl')[i][6] == 1 and record.ask_record_by_account('jl')[i][7] == 1:
        borrow['status'] = '已归还'
    if borrow['status'] == '预约未借阅':
        borrow['time_1'] = '未借阅'
        borrow['time_2'] = '未借阅'
    if borrow['status'] == '借阅中':
        borrow['time_1'] = record.ask_record_by_account('jl')[i][3]
        borrow['time_2'] = '未归还'
    if borrow['status'] == '已归还':
        borrow['time_1'] = record.ask_record_by_account('jl')[i][3]
        borrow['time_2'] = record.ask_record_by_account('jl')[i][3]
    borrow_list.append(borrow)
print(borrow_list)
