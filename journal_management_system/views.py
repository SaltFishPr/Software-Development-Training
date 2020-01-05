from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from database import user


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

    }
    data = {
        'dict': dict1
    }
    # 执行数据库的插入操作
    if (user.check_account_exsit(account) == True):  # 如果存在相同的账户
        dict1['flag'] = 0
    else:
        user.add_user(account, password, name, identity, grade)
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
    if (user.check_account_exsit(Username) == False):
        dict1['flag'] = -1
    else:
        if (user.check_password_exsit(Username) == str(Password)):
            dict1['flag'] = 1
            if user.ask_user_identity(Username) == 'admin':
                dict1['flag'] = 2
            elif user.ask_user_identity(Username) == 'journal_admin':
                dict1['flag'] = 3

        else:
            dict1['flag'] = 0
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
    name = user.ask_user_name(account)
    grarde = user.ask_user_grade(account)
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
    borrow = dict()
    borrow['name'] = 'science'
    borrow['status'] = '借阅中'
    borrow['time_1'] = '1点'
    borrow['time_2'] = '未归还'
    borrow_list.append(borrow)
    borrow = dict()
    borrow['name'] = 'nature'
    borrow['status'] = '已经归还'
    borrow['time_1'] = '1点'
    borrow['time_2'] = '2点'
    borrow_list.append(borrow)
    print(borrow_list)
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
        if name==user.get_name_by_account(account):
            dict1['flag'] = 0
            return JsonResponse(data)
        user.update_user_password(account,pwd)
    elif pwd =="":
        if pwd==user.check_password_exsit(account):
            dict1['flag']=0
            return JsonResponse(data)
        user.update_user_name(account,name)
    else:
        if name == user.get_name_by_account(account):
            if pwd == user.check_password_exsit(account):
                dict1['flag'] = 0
                return JsonResponse(data)
            else:
                user.update_user_password(account, pwd)
        else:
            if pwd == user.check_password_exsit(account):
                user.update_user_name(account, name)
            else:
                user.update_user_password(account, pwd)
                user.update_user_name(account, name)
    dict1['flag'] = 1
    return JsonResponse(data)
