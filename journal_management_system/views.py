from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from backstage.contorl import JsonPack


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
    # dict1 = {
    #     'flag':-1
    # }
    # data = {
    #     'dict': dict1
    # }
    # # 执行数据库的插入操作
    # if (UserDB.check_user_exist(account)):  # 如果存在相同的账户
    #     dict1['flag'] = 0
    # else:
    #     UserDB.add_user(account, password, name, identity, grade)
    #     dict1['flag'] = 1
    data = JsonPack.register_check(account, password, name, identity, grade)
    return JsonResponse(data)


# 跳转到登陆界面
def register_return(request):
    return render(request, 'login_page.html')


# 跳转到登陆界面
def login_page(request):
    return render(request, 'login_page.html')


# 确认登陆
def login_judge(request):
    user_name = str(request.GET.get('username'))
    pass_word = str(request.GET.get('password'))

    # if (user.UserDB.check_account(Username,Password) == str(Password)):
    #     dict1['flag'] = 1
    #     if user.UserDB.check_account(Username,Password) == 'admin':
    #         dict1['flag'] = 2
    #     elif user.UserDB.check_account(Username,Password) == 'journal_admin':
    #         dict1['flag'] = 3
    #
    # else:
    #     dict1['flag'] = 0
    data = JsonPack.login_check(user_name, pass_word)
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
    data = JsonPack.get_reader_center_info(account)
    return JsonResponse(data)


# 用户数据更新
def user_data_update(request):
    account = request.get_signed_cookie('account', salt='666')
    name = request.GET.get('username')
    pwd = request.GET.get('password')
    data = JsonPack.update_user_check(account, name, pwd)
    return JsonResponse(data)


# 得到期刊的信息
def journal_search_load(request):
    data = JsonPack.get_journal_info()
    return JsonResponse(data)


# 根据年搜索期刊

def journal_name_search(request):
    name = request.GET.get('name')
    data = JsonPack.get_journal_year(name)
    return JsonResponse(data)


def journal_year_search(request):
    name = request.GET.get('name')
    year = int(request.GET.get('year'))
    data = JsonPack.get_journal_stage(name, year)
    return JsonResponse(data)


def journal_stage_search(request):
    name = request.GET.get('name')
    year = int(request.GET.get('year'))
    stage = int(request.GET.get('stage'))
    data = JsonPack.confirm_journal(name, year, stage)
    return JsonResponse(data)
