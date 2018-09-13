# -*- coding:utf-8 -*-

from django.conf.urls import url
from monitor import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^welcome/', views.welcome),
    url(r'^manager/', views.manager),  # 页面接口
    url(r'^data/', views.tabledata),  # 整表数据接口

    url(r'^update/', views.updatetable),  # 更新接口
    url(r'^delete/', views.deletetable),  # 删除接口

    url(r'^functions/', views.functions),  # 系统功能点

    url(r'^sms/', views.sms_send),  # 发送短信
    url(r'^start/', views.task_start),  # 启动任务
    url(r'^echo/', views.echo_log),  # 获取任务 socket接口

    url(r'^file/', views.file),  # 文件接口
]
