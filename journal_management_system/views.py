from django.http import JsonResponse
from django.shortcuts import render, redirect
from backstage.contorl import JsonPack


# 跳转到注册界面
def register_page(request):
    return render(request, 'sign_up.html')


# 注册确认
def register_judge(request):
    account = request.GET.get('username')
    password = request.GET.get('password')
    # name=request.GET.get('name')
    name = account
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
    return render(request, 'sign_in.html')


# 跳转到登陆界面
def login(request):
    try:
        cur_account = request.get_signed_cookie('account', salt="666")
    except KeyError:
        print('no cookie')
        return render(request, 'sign_in.html')
    else:
        user = JsonPack.get_object_by_account(cur_account)
        print(user.get_self_info('account_name_grade'))
        identity = user.get_identity()
        print(identity)
        if identity == 'reader':
            return render(request, 'reader/main.html')
        elif identity == 'journal_admin':
            return render(request, 'journal_admin/main.html')
        elif identity == 'admin':
            return render(request, 'admin/main.html')


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
    password = request.GET.get('password')
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
    return render(request, 'reader/main.html')


# 跳转到系统管理员中心
def system_admin_center_page(request):
    return render(request, 'admin/main.html')


# 跳转到期刊管理员中心
def journal_admin_center_page(request):
    return render(request, 'journal_admin/main.html')


# 跳转到用户数据界面
def user_data_page(request):
    return render(request, 'reader/personal_information.html')


# 跳转到用户借阅界面
def user_borrow_page(request):
    return render(request, 'reader/borrow_page.html')


def journal_admin_borrow_page(request):
    return render(request, 'journal_admin/borrow_operation.html')


def journal_admin_order_page(request):
    return render(request, 'journal_admin/order_operation.html')


def journal_admin_return_page(request):
    return render(request, 'journal_admin/return_operation.html')


#
def journal_admin_store_page(request):
    return render(request, 'journal_admin/store_operation.html')


def user_center_info(request):
    cur_account = request.get_signed_cookie('account', salt="666")

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
    user = JsonPack.get_object_by_account(cur_account)
    data = user.get_record_info()
    return JsonResponse(data)


# 用户数据更新
def user_data_update(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    name = request.GET.get('username')
    pwd = request.GET.get('password')
    user = JsonPack.get_object_by_account(cur_account)
    data = user.check_info_update(cur_account, name, pwd)
    return JsonResponse(data)


def journal_search_load(request):
    """
    得到所有期刊的信息
    :param request:
    :return:
    """
    data = JsonPack.get_journal_info()
    return JsonResponse(data)


def journal_name_search(request):
    """
    得到该期刊的所有年、期
    :param request:
    :return:
    """
    name = request.GET.get('name')
    data = JsonPack.get_journal_year(name)
    return JsonResponse(data)


def journal_year_search(request):
    """
    得到该期刊、该年的所有期
    :param request:
    :return:
    """
    name = request.GET.get('name')
    year = int(request.GET.get('year'))
    data = JsonPack.get_journal_stage(name, year)
    return JsonResponse(data)


def journal_stage_search(request):
    """
    返回唯一一个期刊
    :param request:
    :return:
    """
    name = request.GET.get('name')
    year = int(request.GET.get('year'))
    stage = int(request.GET.get('stage'))
    data = JsonPack.confirm_journal(name, year, stage)
    return JsonResponse(data)


def user_borrow_info(request):
    """
    返回用户自己的name和Grade
    :param request:
    :return:
    """
    cur_account = request.get_signed_cookie('account', salt='666')
    user = JsonPack.get_object_by_account(cur_account)
    data = user.get_self_info('name_grade')
    return JsonResponse(data)


def user_data_info(request):
    """
    返回用户自己的account,name,grade
    :param request:
    :return:
    """
    cur_account = request.get_signed_cookie('account', salt='666')
    user = JsonPack.get_object_by_account(cur_account)
    data = user.get_self_info('account_name_grade')
    return JsonResponse(data)


def admin_info(request):
    """

    :param request:
    :return:
    """
    cur_account = request.get_signed_cookie('account', salt='666')
    user = JsonPack.get_object_by_account(cur_account)
    data = user.get_self_info('account_name_grade')
    return JsonResponse(data)


def admin_user_update(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    user = JsonPack.get_object_by_account(cur_account)
    account = request.GET.get('account')
    name = request.GET.get('name')
    grade = (request.GET.get('grade'))
    identity = request.GET.get('identity')
    data = user.modify_user_info(account, name, grade, identity)
    return JsonResponse(data)


def admin_users_info(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    user = JsonPack.get_object_by_account(cur_account)
    data = user.get_user_info_group_by_identity()
    return JsonResponse(data)


def account_select_load(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    user = JsonPack.get_object_by_account(cur_account)
    data = user.get_all_user_info()
    return JsonResponse(data)


def account_info_load(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    account = request.GET.get('account')
    user = JsonPack.get_object_by_account(cur_account)
    data = user.get_data_by_account(account)
    return JsonResponse(data)


def user_register(request):
    account = request.GET.get('account')
    password = request.GET.get('password')
    name = request.GET.get('name')
    identity = request.GET.get('identity')
    grade = int(request.GET.get('grade'))
    data = JsonPack.register_check(account, password, name, identity, grade)
    return JsonResponse(data)


def user_delete(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    account = request.GET.get('account')
    user = JsonPack.get_object_by_account(cur_account)
    data = user.remove_account(account)
    return JsonResponse(data)


def journal_admin_info(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    journal_admin = JsonPack.get_object_by_account(cur_account)
    data = journal_admin.get_journal_admin_info('all')
    return JsonResponse(data)


def journal_admin_user_borrow_info(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    journal_admin = JsonPack.get_object_by_account(cur_account)
    data = journal_admin.get_journal_admin_info('borrow')
    return JsonResponse(data)


def journal_admin_user_order_info(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    journal_admin = JsonPack.get_object_by_account(cur_account)
    data = journal_admin.get_journal_admin_info('order')
    return JsonResponse(data)


def journal_admin_user_return_info(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    journal_admin = JsonPack.get_object_by_account(cur_account)
    data = journal_admin.get_journal_admin_info('borrow')
    return JsonResponse(data)


def record_update(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    user = JsonPack.get_object_by_account(cur_account)
    account = request.GET.get('user_name')
    journal_name = request.GET.get('journal_name')
    journal_year = int(request.GET.get('journal_year'))
    journal_stage = int(request.GET.get('journal_stage'))
    record_operation = request.GET.get('record_update_method')
    print(record_operation)
    data = user.record_update(account, journal_name, journal_year, journal_stage, record_operation)
    return JsonResponse(data)


def journal_update(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    user = JsonPack.get_object_by_account(cur_account)
    journal_name = request.GET.get('journal_name')
    journal_year = int(request.GET.get('journal_year'))
    journal_stage = int(request.GET.get('journal_stage'))
    record_operation = request.GET.get('record_update_method')
    journal_num = int(request.GET.get('journal_num'))
    data = user.journal_total_num_update(journal_name, journal_year, journal_stage, record_operation, journal_num)
    print(data)
    return JsonResponse(data)


def user_journal_order(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    user = JsonPack.get_object_by_account(cur_account)
    journal_name = (request.GET.get('journal_name'))
    print(request.GET.get('journal_name'))
    print(request.GET.get('journal_year'))
    print(request.GET.get('journal_stage'))
    journal_year = int(request.GET.get('journal_year'))
    journal_stage = int(request.GET.get('journal_stage'))
    data = user.order(journal_name, journal_year, journal_stage)
    print(data)
    return JsonResponse(data)


def sign_out(request):
    rep = redirect('/login')
    rep.delete_cookie('account')
    return rep


def record_table_by_user_name(request):
    account = request.GET.get('user_name')
    status = request.GET.get('status')
    data = JsonPack.get_record_by_account(account, status)
    return JsonResponse(data)


def record_table_by_journal_name(request):
    journal_name = request.GET.get('journal_name')
    status = request.GET.get('status')
    data = JsonPack.get_record_by_journal_name(journal_name, status)
    return JsonResponse(data)


def journal_admin_7days_record(request):
    data = JsonPack.line_chart_data()
    return JsonResponse(data)


def user_name_datalist(request):
    cur_account = request.get_signed_cookie('account',salt='666')
    user = JsonPack.get_object_by_account(cur_account)
    data = user.get_order_user_info()
    return JsonResponse(data)

def journal_name_datalist(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    user = JsonPack.get_object_by_account(cur_account)
    data = user.get_journal_name_info()
    print(data)
    return JsonResponse(data)


def journal_table_by_journal_name(request):
    cur_account = request.get_signed_cookie('account', salt='666')
    journal_name = request.GET.get('journal_name')
    user = JsonPack.get_object_by_account(cur_account)
    data = user.get_journal_info_by_name(journal_name)
    return JsonResponse(data)



