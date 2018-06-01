# -*- coding:utf-8 -*-
import schedule
import time
from threading import Thread
from monitor.models import TaskList, SysParam
from monitor.util.taskEngine import TaskEngine


# https://blog.csdn.net/kamendula/article/details/51452352
class MySchedule(Thread):
    def __init__(self, parent=None):
        super(MySchedule, self).__init__(parent)
        self.ploy_code = dict(SysParam.objects.filter(flag=1, code='ploy_code').values_list('param', 'memo'))
        self.tasklist = TaskList.objects.filter(type='1', up=0).exclude(ploy='').values('no', 'ploy', 'time_set')

    def run_thread(self, task_no):
        te = TaskEngine(task_no)
        te.start()

    def sched(self):
        for i in self.tasklist:
            if i['ploy'] == '1':
                exec('schedule.every(' + i['time_set'] + ').seconds.do(self.run_thread,' + str(i['no']) + ')')
            else:
                exec('schedule.every().' + self.ploy_code[i['ploy']] + '.at("' + i['time_set'] + '").do(self.run_thread,' + str(i['no']) + ')')

    def run(self):
        while True:
            schedule.run_pending()
