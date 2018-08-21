# -*- coding:utf-8 -*-
from jpype import *
from threading import Thread
from django.db import connection
from monitor.util.preload import logger, q
from monitor.models import SMSLog
import datetime, time
import schedule


class SMS:
    def __init__(self):
        jarpath = 'static/lib/jar/ediClient-2017-02-17.jar'
        dependency = 'static/lib/jar/dependency'
        if not isJVMStarted():
            startJVM("static/lib/jre7/bin/client/jvm.dll", "-Xint", "-Djava.class.path=%s" % jarpath, "-Djava.ext.dirs=%s" % dependency)
        attachThreadToJVM()  # django是多线程,必须加入这一条,不然就必须多次启动JVM
        # java.lang.System.out.println("hello World")
        self.EDIClient = JClass('com.csg.itms.edic.util.client.EDIClient')
        self.MsgHandler = JClass('com.csg.itms.edic.util.client.MsgHandler')
        self.Request = JClass('com.csg.itms.edic.util.message.Request')
        self.Response = JClass('com.csg.itms.edic.util.message.Response')

    def send_sms(self, server='10.150.68.133', port=60001, subject='SOA2NARIAlertSend', classname='SystemManage', sence='SOA', **kwargs):
        map = JClass("java.util.HashMap")()
        map.put("CLASSNAME", classname)  # 约定为安全审计系统集成大类
        map.put("SCENE", sence)  # 以启明星辰为例
        map.put("TIME", kwargs['time'])  # 本消息生成时间
        map.put("AREACODE", kwargs['areacode'])  # 单位以超高压输电公司本部为例
        map.put("MAINDATA", kwargs['maindata'])  # 告警主数据，”AlarmID=$SOC平台告警ID”
        map.put("ID", kwargs['policy'])  # 按照ITSM的配置项编码标准
        map.put("OriginalID", kwargs['originalid'])  # 按照ITSM的配置项编码标准
        map.put("IPAddress", kwargs['ipaddress'])  # 产生告警配置项的IP地址
        map.put("AlarmID", kwargs['alarmid'])  # SOC平台的告警ID
        map.put("AlarmCate", kwargs['alarmcate'])  # 安全告警
        map.put("AlarmLevel", kwargs['alarmlevel'])  # 重大告警
        map.put("AlarmType", kwargs['alarmtype'])  # 描述告警
        map.put("AlarmContent", kwargs['alarmcontent'])  # 告警内容描述
        map.put("AlarmStatus", kwargs['alarmstatus'])  # 未确认状态
        map.put("AlarmCount", str(kwargs['alarmcount']))  # 告警重复次数
        map.put("FirstTime", kwargs['firsttime'])  # 告警开始时间
        map.put("EndTime", kwargs['endtime'])  # 告警结束时间

        client = self.EDIClient(server, int(port))
        sessionId = client.authenticate("", "")
        r = self.Request()
        r.setContent(map)
        r.setSessionId(str(sessionId))
        r.setSubject(str(subject))
        r = self.MsgHandler.sealMessage(r)
        response = client.sendMesssage(r)
        if response.isSuccessful():
            return True
        else:
            return False


class SMSSender:
    def __init__(self):
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
                            now() AS time,
                            min(alarmtime) AS firsttime,
                            max(alarmtime) AS endtime 
                        FROM monitor_policylog 
                        WHERE alarmlevel = '%s'
                        and AlarmTime between '%s' and '%s'
                        GROUP BY func_id,task_id,step_id,alarmlevel,alarmcontent,policy_id) AS t
                        GROUP BY policy,originalid,maindata,alarmid,alarmlevel,alarmcount,alarmcount,alarmcate,
                        alarmtype,alarmstatus,ipaddress,time,firsttime,endtime"""
        self.level_01 = 60
        self.level_02 = 30
        self.level_03 = 15
        self.level_04 = 5

    def dictfetchall(self, cursor):
        # 将游标返回的结果保存到一个字典对象中
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

    def sms_level_01(self):  # 提示告警
        now = datetime.datetime.now()
        start_time = (now - datetime.timedelta(minutes=self.level_01)).strftime('%Y/%m/%d %H:%M:%S')
        end_time = now.strftime('%Y/%m/%d %H:%M:%S')
        cursor = connection.cursor()
        cursor.execute(self.sql % ('01', start_time, end_time))
        result = self.dictfetchall(cursor)
        self.sms_send(result)

    def sms_level_02(self):  # 一般告警
        now = datetime.datetime.now()
        start_time = (now - datetime.timedelta(minutes=self.level_02)).strftime('%Y/%m/%d %H:%M:%S')
        end_time = now.strftime('%Y/%m/%d %H:%M:%S')
        cursor = connection.cursor()
        cursor.execute(self.sql % ('02', start_time, end_time))
        result = self.dictfetchall(cursor)
        self.sms_send(result)

    def sms_level_03(self):  # 重大告警
        now = datetime.datetime.now()
        start_time = (now - datetime.timedelta(minutes=self.level_03)).strftime('%Y/%m/%d %H:%M:%S')
        end_time = now.strftime('%Y/%m/%d %H:%M:%S')
        cursor = connection.cursor()
        cursor.execute(self.sql % ('03', start_time, end_time))
        result = self.dictfetchall(cursor)
        self.sms_send(result)

    def sms_level_04(self):  # 紧急告警
        now = datetime.datetime.now()
        start_time = (now - datetime.timedelta(minutes=self.level_04)).strftime('%Y/%m/%d %H:%M:%S')
        end_time = now.strftime('%Y/%m/%d %H:%M:%S')
        cursor = connection.cursor()
        cursor.execute(self.sql % ('04', start_time, end_time))
        result = self.dictfetchall(cursor)
        self.sms_send(result)

    def sms_send(self, result):
        for i in result:
            SMSLog.objects.create(**i)
            SMS().send_sms(**i)
            logger.info('短信已发送...')

    def sched(self):
        time.sleep(1)
        schedule.every(self.level_01).minutes.do(self.sms_level_01)
        schedule.every(self.level_02).minutes.do(self.sms_level_02)
        schedule.every(self.level_03).minutes.do(self.sms_level_03)
        schedule.every(self.level_04).minutes.do(self.sms_level_04)
