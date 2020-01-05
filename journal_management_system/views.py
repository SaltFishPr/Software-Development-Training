from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from database import user


def register_page(request):
    return render(request,'user_register_page.html')

def register_judge(request):
    account = request.GET.get('username')
    password=request.GET.get('password')
    #name=request.GET.get('name')
    name='OvO'
    identity='reader'
    grade=1
    dict1={

    }
    data={
        'dict':dict1
    }
    #执行数据库的插入操作
    if(user.check_account_exsit(account)==True):#如果存在相同的账户
        dict1['flag']=0
    else:
        user.add_user(account, password, name, identity, grade)
        dict1['flag']=1
    return JsonResponse(data)
def register_return(request):
    return render(request,'login_page.html')
def login_page(request):
    return render(request,'login_page.html')
def login_judge(request):
    dict1={
        'flag':-1
    }
    data={
        'dict':dict1,
        'pageTitle':8798,
        'pageData':66
    }
    Username = str(request.GET.get('username'))
    Password = str(request.GET.get('password'))
    if(user.check_account_exsit(Username)==False):
        dict1['flag'] = -1
    else:
        if(user.check_password_exsit(Username)==str(Password)):
            dict1['flag'] = 1
            if user.ask_user_identity(Username) == 'admin':
                dict1['flag'] = 2
            elif user.ask_user_identity(Username) == 'journal_admin':
                dict1['flag'] = 3

        else:
            dict1['flag'] = 0
    print(dict1['flag'])
    return JsonResponse(data)
def login_return(request):
    password = (request.GET.get('password'))
    username=request.GET.get('username')
    if password=='1':
        rep=redirect('/user_center_page')
    elif password=='2':
        rep = redirect('/system_admin_center_page')
    else:
        rep = redirect('/journal_admin_center_page')
    rep.set_signed_cookie('account', username, salt='666')
    return rep

def user_center_page(request):
     return render(request,'user_center_page.html')
def system_admin_center_page(request):
    return render(request,'system_admin_center_page.html')
def journal_admin_center_page(request):
    return render(request,'journal_admin_center_page.html')
def user_data_page(request):
    return render(request,'user_data_page.html')
def user_borrow_page(request):
    return render(request,'user_borrow_page.html')
def journal_admin_store_page(request):
    return render(request,'journal_admin_store_page.html')