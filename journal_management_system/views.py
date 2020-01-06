from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from database.user import UserDB
from database.record import RecordDB
from database.journal import JournalDB

# 跳转到注册界面
def register_page(request):
    return render(request, 'user_register_page.html')


# 注册确认
def register_judge(request):
    account = request.GET.get('username')
    password = request.GET.get('password')
    # name=request.GET.get('name')
    name = 'OvO'
    identity = 'reader'
    grade = 1
    dict1 = {
        'flag':-1
    }
    data = {
        'dict': dict1
    }
    # 执行数据库的插入操作
    if (UserDB.check_user_exist(account)):  # 如果存在相同的账户
        dict1['flag'] = 0
    else:
        UserDB.add_user(account, password, name, identity, grade)
        dict1['flag'] = 1
    return JsonResponse(data)


# 跳转到登陆界面
def register_return(request):
    return render(request, 'login_page.html')


# 跳转到登陆界面
def login_page(request):
    return render(request, 'login_page.html')


# 确认登陆
def login_judge(request):
    dict1 = {
        'flag': -1
    }
    data = {
        'dict': dict1,
        'pageTitle': 8798,
        'pageData': 66
    }
    Username = str(request.GET.get('username'))
    Password = str(request.GET.get('password'))
    if (UserDB.check_account(Username,Password) == False):
        dict1['flag'] = -1
    else:
        if UserDB.get_user_identity(Username) =='admin':
            dict1['flag'] = 2
        elif UserDB.get_user_identity(Username) =='journal_admin':
            dict1['flag'] =3
        else:
            dict1['flag'] = 1
        # if (user.UserDB.check_account(Username,Password) == str(Password)):
        #     dict1['flag'] = 1
        #     if user.UserDB.check_account(Username,Password) == 'admin':
        #         dict1['flag'] = 2
        #     elif user.UserDB.check_account(Username,Password) == 'journal_admin':
        #         dict1['flag'] = 3
        #
        # else:
        #     dict1['flag'] = 0
    return JsonResponse(data)


# 确定登陆权限
def login_return(request):
    password = (request.GET.get('password'))
    username = request.GET.get('username')
    if password == '1':
        rep = redirect('/user_center_page')
    elif password == '2':
        rep = redirect('/system_admin_center_page')
    else:
        rep = redirect('/journal_admin_center_page')
    rep.set_signed_cookie('account', username, salt='666')
    return rep


# 跳转到用户中心
def user_center_page(request):
    ret = request.get_signed_cookie('account', salt="666")
    print(ret)
    return render(request, 'user_center_page.html')


# 跳转到系统管理员中心
def system_admin_center_page(request):
    return render(request, 'system_admin_center_page.html')


# 跳转到期刊管理员中心
def journal_admin_center_page(request):
    return render(request, 'journal_admin_center_page.html')


# 跳转到用户数据界面
def user_data_page(request):
    return render(request, 'user_data_page.html')


# 跳转到用户借阅界面
def user_borrow_page(request):
    return render(request, 'user_borrow_page.html')


#
def journal_admin_store_page(request):
    return render(request, 'journal_admin_store_page.html')


def user_center_info(request):
    account = request.get_signed_cookie('account', salt="666")
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
    info_len=RecordDB.get_info_length(account)
    key_list = RecordDB.get_key_by_account(account)
    for i in range(info_len):
        borrow = dict()
        borrow['name'] = JournalDB.get_name_by_key(key_list[i])
        # 1 0 0预约未借阅
        # x 1 0  借阅 未归还
        # x 1 1 归还
        if RecordDB.get_record_by_account(account)[i][5] == 1 and RecordDB.get_record_by_account(account)[i][6] == 0 and \
                RecordDB.get_record_by_account(account)[i][7] == 0:
            borrow['status'] = '预约未借阅'
        elif RecordDB.get_record_by_account(account)[i][6] == 1 and RecordDB.get_record_by_account(account)[i][7] == 0:
            borrow['status'] = '借阅中'
        elif RecordDB.get_record_by_account(account)[i][6] == 1 and RecordDB.get_record_by_account(account)[i][7] == 1:
            borrow['status'] = '已归还'
        else:
            borrow['status']='异常情况'
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
            borrow['time_1']='异常情况'
            borrow['time_2']='异常情况'
        borrow_list.append(borrow)
    # borrow = dict()
    # borrow['name'] = 'science'
    # borrow['status'] = '借阅中'
    # borrow['time_1'] = '1点'
    # borrow['time_2'] = '未归还'
    # borrow_list.append(borrow)
    # borrow = dict()
    # borrow['name'] = 'nature'
    # borrow['status'] = '已经归还'
    # borrow['time_1'] = '1点'
    # borrow['time_2'] = '2点'
    # borrow_list.append(borrow)
    # print(borrow_list)
    data = {
        'user_info': user_info,
        'borrow_list': borrow_list
    }
    return JsonResponse(data)


def user_data_update(request):
    account=request.get_signed_cookie('account',salt='666')
    name=request.GET.get('username')
    pwd=request.GET.get('password')
    dict1 = {
        'flag': -1
    }
    data = {
        'dict': dict1
    }
    if name =="":
        if name==UserDB.get_user_name(account):
            dict1['flag'] = 0
            return JsonResponse(data)
        UserDB.update_user_password(account,pwd)
    elif pwd =="":
        if pwd==UserDB.get_user_password(account):
            dict1['flag']=0
            return JsonResponse(data)
        UserDB.update_user_name(account,name)
    else:
        if name == UserDB.get_user_name(account):
            if pwd == UserDB.get_user_password(account):
                dict1['flag'] = 0
                return JsonResponse(data)
            else:
                UserDB.update_user_password(account, pwd)
        else:
            if pwd == UserDB.get_user_password(account):
                UserDB.update_user_name(account, name)
            else:
                UserDB.update_user_password(account, pwd)
                UserDB.update_user_name(account, name)
    dict1['flag'] = 1
    return JsonResponse(data)
