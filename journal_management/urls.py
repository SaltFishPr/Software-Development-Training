"""journal_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.urls import path
from journal_management_system import views

urlpatterns = [
    path(r'admin/', admin.site.urls),
    # path('', views.page),
    # url('login/', views.login),
    # url('main',views.main),
    #
    # path('chartjs.html', views.test_chartjs),
    # path('basic_elements.html', views.test_basic_elements),
    # path('font-awesome.html', views.test_icon),
    # url('index_v1', views.test)

    url('login_page', views.login_page),
    url('login_judge', views.login_judge),
    url('login_return', views.login_return),
    url('register_judge', views.register_judge),
    url('register_return', views.register_return),
    url('register_page', views.register_page),
    url('user_center_page', views.user_center_page),
    url('system_admin_center_page', views.system_admin_center_page),
    url('journal_admin_center_page', views.journal_admin_center_page),
    url('user_data_page', views.user_data_page),
    url('user_borrow_page', views.user_borrow_page),
    url('journal_admin_store_page', views.journal_admin_store_page),
    url('user_center_info', views.user_center_info),
    url('user_data_update', views.user_data_update),
    url('journal_search_load', views.journal_search_load),
    url('journal_name_search', views.journal_name_search),
    url('journal_year_search', views.journal_year_search),
    url('journal_stage_search', views.journal_stage_search),
    url('user_borrow_info',views.user_borrow_info),
    url('user_data_info',views.user_data_info),
    url('admin_info',views.admin_info),
    url('admin_user_update',views.admin_user_update),
    url('admin_users_info',views.admin_users_info),
    url('account_select_load',views.account_select_load),
    url('user_name_update',views.admin_user_update),
    url('user_grade_update',views.admin_user_update),
    url('user_identity_update',views.admin_user_update),
    url('account_info_load',views.account_info_load),
    url('', views.login_page)
]
