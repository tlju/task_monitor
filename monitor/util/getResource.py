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
from monitor.models import Variable, TaskList, TaskListConfig


def task_start(no):
    task_type = TaskList.objects.filter(no=no).exclude(type='2').values()[0]['type']  # 获取任务类别，根据类别来分别执行
    sub_task = list(TaskList.objects.filter(up=no).exclude(type='2').values('no'))
    task_variable = list(Variable.objects.filter(type__in=['1', '2'], task__in=[-1, no]).values('code', 'value', 'name'))
    if len(sub_task):
        task_variable += list(Variable.objects.filter(type='2', task__in=[x['no'] for x in sub_task]).values('code', 'value', 'name'))
        task_variable = [dict(t) for t in {tuple(d.items()) for d in task_variable}]  # 列表字典去重 https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
        task_variable = translate(task_variable)
        if task_type == '3':  # 批量
            task_step = TaskList.objects.filter(type='2', up__in=[x['no'] for x in sub_task]).values()
            task_step_param = TaskListConfig.objects.filter(task__in=[x['no'] for x in sub_task]).values()
            t = TaskEngine(no, task_variable, task_step, task_step_param)
            t.start()
        elif task_type == '4':  # 循环
            start, end, date_type = None, None, None
            for i in task_variable:
                if i['code'] == '@loop_start_date':
                    start = datetime.datetime.strptime(i['value'], i['name'])
                    date_type = i['name']
                elif i['code'] == '@loop_end_date':
                    end = datetime.datetime.strptime(i['value'], i['name'])
                elif i['code'] == '@loop_start_num':
                    start = i['value']
                elif i['code'] == '@loop_end_num':
                    end = i['value']
            # print(start, end) start.strftime(date_type)
            current_variable_all = []
            if not str(start).isdigit():
                while start <= end:
                    current_variable = []
                    for x, y in enumerate(task_variable):
                        # print(x,y,y['value'].replace('@current',start.strftime(date_type)))
                        current_variable.append({'code': y['code'], 'name': y['name'], 'value': y['value'].replace('@current', start.strftime(date_type))})
                        current_variable.append({'code': '@current', 'name': '当前循环值', 'value': start.strftime(date_type)})
                    # print(current_variable)
                    current_variable_all.append(current_variable)
                    start += datetime.timedelta(days=1)
            else:
                while start <= end:
                    current_variable = []
                    for x, y in enumerate(task_variable):
                        current_variable.append({'code': y['code'], 'name': y['name'], 'value': y['value'].replace('@current', start)})
                        current_variable.append({'code': '@current', 'name': '当前循环值', 'value': start})
                    current_variable_all.append(current_variable)
                    start += 1
            task_step = TaskList.objects.filter(type='2', up__in=[x['no'] for x in sub_task]).values()
            task_step_param = TaskListConfig.objects.filter(task__in=[x['no'] for x in sub_task]).values()
            # print(current_variable_all)
            threads = []
            for i in sub_task:
                for variable in current_variable_all:
                    # print(i['no'], 'variable:',variable, 'task_step:',task_step, 'task_step_param:',task_step_param)
                    t = TaskEngine(i['no'], variable, task_step, task_step_param)
                    t.setDaemon(True)
                    threads.append(t)
            # print(threads)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
    else:
        task_step = TaskList.objects.filter(type='2', up=no).values()
        task_step_param = TaskListConfig.objects.filter(task=no).values()
        t = TaskEngine(no, task_variable, task_step, task_step_param)
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
    status = 0
    table = ''
    allmenu = cache.get('allmenu')
    for i in allmenu:
        if i['code'] == int(code): table = i['table']
    cls = import_table(table)
    up_data = json.loads(data)
    if not up_data['id']:
        if table == 'TaskList':
            if up_data['condition']['type'] == '1' or up_data['condition']['type'] == '3' or up_data['condition']['type'] == '4':
                no_max = cls.objects.filter(up=0).aggregate(Max('no'))['no__max']
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
            elif up_data['condition']['type'] == '5':
                if not up_data['condition'].get('no'):
                    no_max = cls.objects.filter(up=0).aggregate(Max('no'))['no__max']
                    if no_max:
                        cls.objects.create(no=no_max + 1, up=0, **up_data['condition'])
                        update_variable(no_max + 1, up_data['condition']['param'])  # 更新自定义参数表
                    else:
                        cls.objects.create(no=1, up=0, **up_data['condition'])
                        update_variable(1, up_data['condition']['param'])  # 更新自定义参数表
                else:
                    cls.objects.create(**up_data['condition'])
        elif table == 'TaskListConfig':
            up_data['condition']['value'] = json.dumps(up_data['condition']['value'])  # 存到数据库为json字符串
            cls.objects.create(**up_data['condition'])
        else:
            cls.objects.create(**up_data['condition'])
    else:
        if table == 'TaskList':
            no = list(cls.objects.filter(id=str(up_data['id'])).values('no'))[0]['no']
            if 'param' in up_data['condition']:
                update_variable(no, up_data['condition']['param'])  # 更新自定义参数表

        for k, v in up_data['condition'].items():
            if table == 'TaskListConfig':
                exec_str = 'cls.objects.filter(id=' + str(up_data['id']) + ').update(%s=%s)' % (k, v)  # 转义特殊字符escape(v.replace('\n', '\\n'))
            else:
                exec_str = 'cls.objects.filter(id=' + str(up_data['id']) + ').update(%s="%s")' % (k, v)  # 转义特殊字符escape(v.replace('\n', '\\n'))
            exec(exec_str.replace('\n', '\\n'))  # 执行字符串python语句
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


def update_variable(task_no, variable_param, type='2'):
    # print(task_no, variable_param)
    Variable.objects.filter(task=task_no, type=type).delete()
    if variable_param or variable_param.count('@') >= 1:
        for i in variable_param.split('\n'):
            try:
                Variable.objects.create(
                    **{'value': i.split('=')[1][:-1], 'code': i.split('=')[0].split('|')[0], 'name': i.split('=')[0].split('|')[1], 'type': type, 'task': task_no})
            except Exception:
                print('Variable error')


# 翻译特殊代码
def translate(variable):
    variables = []
    for i in variable:
        if i['code'] == '@day':
            if not i['value']:
                i['value'] = time.strftime('%Y%m%d', time.localtime(time.time()))
        elif i['code'] == '@2-yesterday-nyr':
            now_time = datetime.datetime.now()
            yes_time = now_time + datetime.timedelta(days=-1)
            yes_time_nyr = yes_time.strftime('%Y%m%d')
            if not i['value']:
                i['value'] = yes_time_nyr[:4] + '年' + yes_time_nyr[4:6] + '月' + yes_time_nyr[6:] + '日'
        elif i['code'] == '@yesterday':
            now_time = datetime.datetime.now()
            yes_time = now_time + datetime.timedelta(days=-1)
            yes_time_nyr = yes_time.strftime('%Y%m%d')
            if not i['value']:
                i['value'] = yes_time_nyr
        elif i['code'] == '@yes-nyr':
            now_time = datetime.datetime.now()
            yes_time = now_time + datetime.timedelta(days=-1)
            yes_time_nyr = yes_time.strftime('%Y%m%d')
            if not i['value']:
                i['value'] = yes_time_nyr[:4] + '-' + yes_time_nyr[4:6] + '-' + yes_time_nyr[6:]

        if '@' in i['value']:
            for y in variables:
                if y['code'] in i['value']:
                    i['value'] = i['value'].replace(y['code'], y['value'])
        variables.append(i)
    return variables
