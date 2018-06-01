# -*- coding:utf-8 -*-
import time, datetime
from threading import Thread
from monitor.util.preload import q
from monitor.models import PolicyLog
from monitor.alarm.sms import SMS


class Alarm(Thread):
    def __init__(self, parent=None):
        super(Alarm, self).__init__(parent)

    def start_alarm(self):
        while True:
            item = q.get()
            if item[0] == 1:
                item[0] = '04'
            elif item[0] == 2:
                item[0] = '03'
            elif item[0] == 3:
                item[0] = '02'
            elif item[0] == 4:
                item[0] = '01'
            PolicyLog.objects.create(alarmlevel=item[0], func_id=item[1], alarmtime=item[2], alarmcontent=item[3], task_id=item[4], step_id=item[5],
                                     policy_id=item[6])
            q.task_done()
            time.sleep(0.1)

    def run(self):
        self.start_alarm()
        q.join()  # 阻塞直至所有线程queue.task_done()返回
