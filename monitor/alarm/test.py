# -*- coding:utf-8 -*-
from threading import Thread
from django.db import connection
import schedule,datetime,time


class SMSSender(Thread):
    def __init__(self, parent=None):
        super(SMSSender, self).__init__(parent)
        self.sql = """SELECT
                        policy,originalid,maindata,alarmid,alarmlevel,areacode,
                        GROUP_CONCAT(alarmcontent, ';') AS alarmcontent,
                        alarmcount,alarmcate,alarmtype,alarmstatus,ipaddress,time,firsttime,endtime 
                        FROM (SELECT
                            'S' || policy_id || '-' || task_id || '-' || step_id AS policy,
                            'S' || policy_id || '-' || task_id || '-' || step_id AS originalid,
                            'AlarmID=A' || policy_id AS maindata,
                            'A' || policy_id AS alarmid,
                            alarmlevel,alarmcontent,
                            count(1) AS alarmcount,
                            '08' AS alarmcate,'01' AS alarmtype,'01' AS alarmstatus,'0300' AS areacode,
                            GROUP_CONCAT(ipaddress, ';') AS ipaddress,
                            datetime ('now', 'localtime') AS time,
                            min(alarmtime) AS firsttime,
                            max(alarmtime) AS endtime 
                        FROM monitor_policylog 
                        WHERE alarmlevel = '%s'
                        and AlarmTime between '%s' and '%s'
                        GROUP BY func_id,task_id,step_id,alarmlevel,alarmcontent,policy_id) 
                        GROUP BY policy,originalid,maindata,alarmid,alarmlevel,alarmcount,alarmcount,alarmcate,
                        alarmtype,alarmstatus,ipaddress,time,firsttime,endtime"""

    def dictfetchall(self, cursor):
        # 将游标返回的结果保存到一个字典对象中
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

    def sms_level_01(self):  # 提示告警
        now = datetime.datetime.now()
        start_time = (now - datetime.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
        end_time = now.strftime('%Y-%m-%d %H:%M:%S')
        cursor = connection.cursor()
        cursor.execute(self.sql % ('01', start_time, end_time))
        result = self.dictfetchall(cursor)
        #print(self.sql % ('01', start_time, end_time))
        print(start_time,end_time)

    def sched(self):
        time.sleep(1)
        # schedule.every(1).hours.do(self.sms_level_01, schedule.next_run().strftime('%Y-%m-%d %H:%M:%S'))
        schedule.every(60).seconds.do(self.sms_level_01)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run(self):
        self.sched()