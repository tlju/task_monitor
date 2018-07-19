# -*- coding:utf-8 -*-
from django.core.cache import cache
from monitor.models import *
from monitor.recordLog import RecordLog
import queue, schedule

q = queue.PriorityQueue()  # 任务优先队列，最低优先
logger = RecordLog().getlog()


def loading():
    logger.info('加载系统菜单......')
    load_allmenu()
    load_menulist()
    logger.info('加载系统代码数据......')
    load_param()
    logger.info('加载字段代码对应数据......')
    load_mapping()
    logger.info('定时任务模块启动......')
    from monitor.util.mySchedule import MySchedule
    MySchedule().sched()
    logger.info('启动策略扫描告警模块......')
    from monitor.alarm.alarmEngine import Alarm
    Alarm().start()
    logger.info('定时短信功能启动......')
    from monitor.alarm.sms import SMSSender
    SMSSender().sched()

    #MySchedule().start()  # 启动所有的job


def load_allmenu():
    menu = list(SysMenu.objects.all().values())
    cache.set('allmenu', menu, None)


def load_menulist():
    allmenu = cache.get('allmenu')
    code = list()
    display_list = list()
    for i in allmenu:
        if i['up_code'] == 0:
            code.append(i)
    for a in code:
        # print(a)
        sub_menulist = list()
        for b in allmenu:
            if b['up_code'] == a['code']:
                sub_menulist.append({'code': b['code'], 'code_name': b['code_name'], 'url': b['url'],
                                     'file_path': b['file_path'],
                                     'icon': b['icon']})
        display_menu = {'code': a['code'], 'code_name': a['code_name'], 'icon': a['icon'],
                        'sub_menu': sub_menulist}
        display_list.append(display_menu)

    cache.set('leftmenu', display_list, None)


def load_param():
    param = list(SysParam.objects.values().filter(flag=1))
    cache.set('allparam', param, None)


def load_mapping():
    alltable = list(SysMapping.objects.values('table').distinct())
    for i in alltable:
        allfield = list(SysMapping.objects.values('field', 'code').filter(table=i['table']))
        cache.set(i['table'], allfield, None)
