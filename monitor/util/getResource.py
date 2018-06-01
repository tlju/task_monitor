# -*- coding:utf-8 -*-
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.html import escape
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db import connection
from django.db.models.aggregates import Max, Min, Count
import json, time, datetime, ast
from monitor.util.taskEngine import TaskEngine
from monitor.models import Variable


def task_start(no):
    t = TaskEngine(no)
    t.start()


def del_tabledata(code, data):
    status = 1
    table = ''
    allmenu = cache.get('allmenu')
    for i in allmenu:
        if i['code'] == int(code): table = i['table']
    cls = import_table(table)
    del_data = json.loads(data)
    # print(del_data)
    if not del_data['id']:
        text = 'cls.objects'
        for k, v in del_data['condition'].items():
            text += '.filter(' + str(k) + '=' + str(v) + ')'
        exec(text + '.delete()')
    else:
        cls.objects.filter(id=del_data['id']).delete()

    return status


# 更新修改后的表格字段内容
def set_tabledata(code, data):
    # print(code, json.loads(data), type(json.loads(data)))
    # print(data)
    status = 0
    table = ''
    allmenu = cache.get('allmenu')
    for i in allmenu:
        if i['code'] == int(code): table = i['table']
    cls = import_table(table)
    up_data = json.loads(data)
    if not up_data['id']:
        if table == 'TaskList':
            if up_data['condition']['type'] == '1':
                no_max = cls.objects.filter(type='1', up=0).aggregate(Max('no'))['no__max']
                if no_max:
                    cls.objects.create(no=no_max + 1, up=0, **up_data['condition'])
                    update_variable(no_max + 1, up_data['condition']['param'])  # 更新自定义参数表
                else:
                    cls.objects.create(no=1, up=0, **up_data['condition'])
                    update_variable(1, up_data['condition']['param'])  # 更新自定义参数表
            elif up_data['condition']['type'] == '2':
                no_max = cls.objects.filter(type='2', up=up_data['condition']['up']).aggregate(Max('no'))['no__max']
                if no_max:
                    cls.objects.create(no=no_max + 1, **up_data['condition'])
                else:
                    cls.objects.create(no=1, **up_data['condition'])
        else:
            cls.objects.create(**up_data['condition'])
    else:
        for k, v in up_data['condition'].items():
            exec_str = 'cls.objects.filter(id=' + str(up_data['id']) + ').update(%s="%s")' % (k, v)  # 转义特殊字符escape(v.replace('\n', '\\n'))
            exec(exec_str.replace('\n', '\\n'))  # 执行字符串python语句
        if table == 'TaskList':
            no = list(cls.objects.filter(id=str(up_data['id'])).values('no'))[0]['no']
            if 'param' in up_data['condition']:
                update_variable(no, up_data['condition']['param'])  # 更新自定义参数表
        status = 1
    return status


# 针对单表查询
def get_tabledata(table, page, limit, condition, columns, keyword, code_class=None):
    # print(condition, columns, keyword)
    cls = import_table(table)
    if condition:
        text = 'cls.objects'
        text_b = '.filter('
        for k, v in json.loads(condition).items():
            text += '.filter(' + str(k) + '=' + str(v) + ')'
        if columns:
            for i in columns.split(','):
                text_b += 'Q(' + i + '__icontains="' + keyword + '")|'
            text = text + text_b[:-1] + ')'
        data = eval(text + '.values()')
        count = eval(text + '.values().count()')
    else:
        text = 'cls.objects'
        text_b = '.filter('
        if columns:
            for i in columns.split(','):
                text_b += 'Q(' + i + '__icontains="' + keyword + '")|'
            text = text + text_b[:-1] + ')'
        # print(text + '.values()')
        data = eval(text + '.values()')
        count = eval(text + '.values().count()')
    if not page: page = 1
    if not limit: limit = count
    paginator = Paginator(data, limit)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    if cache.get(table):  # 日期类型特殊处理，其他翻译字段在参数表里配置
        table_list = list()
        for a in data:
            for b in cache.get(table):
                if b['code'] == 'date':
                    a[b['field']] = utc2local(a[b['field']])
                else:
                    a[b['field']] = get_param(b['code'], a[b['field']])
            table_list.append(a)
        # print(table_list)
        table_data = {'code': 0, 'msg': '', 'count': count, 'data': table_list}
        table_json = json.dumps(table_data, ensure_ascii=False)
        cache.set('table_data', table_list)
    else:
        table_data = {'code': 0, 'msg': '', 'count': count, 'data': list(data)}
        table_json = json.dumps(table_data, ensure_ascii=False)
        cache.set('table_data', list(data))
    return table_json


# 针对执行sql
def get_tabledata_sql(page, limit, sql, param_dict, code_class=None):
    # print(param_dict)
    sql = sql % json.loads(param_dict)
    # print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)  # cursor.execute('select * from monitor_tasklistconfig')

    def dictfetchall(cursor):
        # 将游标返回的结果保存到一个字典对象中
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

    result = dictfetchall(cursor)
    count = 0
    if code_class == 'get_step_param':  # 可以根据code_class来做特殊处理
        data = result
        count = len(data)
    else:
        data = result
        count = len(data)
    if not page: page = 1
    if not limit: limit = count
    paginator = Paginator(data, limit)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    table_data = {'code': 0, 'msg': '', 'count': count, 'data': list(data)}
    # print(table_data)
    table_json = json.dumps(table_data, ensure_ascii=False)
    return table_json


# 根据sys_menu表的code值获取数据
def get_menutitle(code):
    allmenu = cache.get('allmenu')
    # print(allmenu)
    result = dict()
    for i in allmenu:
        if i['code'] == int(code):
            result = i
    return result


# 根据sys_menu表的code值获取上级数据
def get_menutitle_up(code='0'):
    result = ''
    allmenu = cache.get('allmenu')
    up_code = 0
    for a in allmenu:
        if a['code'] == int(code):
            up_code = a['up_code']
    for b in allmenu:
        if b['code'] == up_code:
            result = b['code_name']
    return result


# 获取系统代码表中的参数值
def get_param(code, value):
    allparam = cache.get('allparam')
    result = ''
    for i in allparam:
        if i['code'] == str(code) and i['param'] == str(value):
            result = i['param_name']
        elif i['code'] == str(code) and i['param_name'] == str(value):
            result = i['param']
    return result


# UTC时间转本地时间(+8:00)
def utc2local(utc_st):
    if utc_st:
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)
        utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
        offset = local_time - utc_time
        local_st = utc_st + offset
        local_st = local_st.strftime("%Y-%m-%d %H:%M:%S")
        if local_st[11:] == '00:00:00': local_st = local_st[:10]
        return local_st
    else:
        return None


# 动态反向表
def import_table(name):
    mod = __import__('monitor.models', fromlist=[name])  # 反向导入模块所有包
    cls = getattr(mod, name)  # 获取包里的class类
    return cls


def update_variable(task_no, variable_param):
    # print(task_no, variable_param)
    Variable.objects.filter(task=task_no, type='2').delete()
    if variable_param or variable_param.count('@') >= 1:
        for i in variable_param.split('\n'):
            try:
                Variable.objects.create(
                    **{'value': i.split('=')[1][:-1], 'code': i.split('=')[0].split('|')[0], 'name': i.split('=')[0].split('|')[1], 'type': '2', 'task': task_no})
            except Exception:
                print('Variable error')
