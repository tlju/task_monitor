#!/usr/bin/python
# -*- coding:utf-8 -*-
# 生成任务文件功能
from monitor.util.allClass import *
from monitor.util.preload import logger, q
from django.db.models import Q
from threading import Thread
from monitor.models import TaskList, TaskListConfig, Functions, FunctionsParam, FunctionsType, Variable, FunctionsPolicy
import ast


class TaskEngine(Thread):
    def __init__(self, task_id, parent=None):
        super(TaskEngine, self).__init__(parent)
        self.task_id = task_id
        self.func = Functions.objects.all().values()
        self.func_param = FunctionsParam.objects.all().values()
        self.func_type = FunctionsType.objects.all().values()
        self.func_policy = FunctionsPolicy.objects.all().values()
        self.task_step = TaskList.objects.filter(type='2', up=self.task_id).values()
        self.task_step_param = TaskListConfig.objects.filter(task=self.task_id).values()
        self.task_variable = self.translate(Variable.objects.filter(Q(task__exact=-1) | Q(task__exact=task_id)).values('code', 'value'))
        self.recv = {}  # 某些函数返回的对象

    def run(self):
        # 功能声明
        # db = DatabaseFunctions('res/init.dat')
        word = WordFunctions()
        other = OtherFunctions()
        excel = ExcelFunctions()
        control = ControlFunctions()
        logic = LogicFunctions()
        ssh = SSHFunctions()
        ws = WebServiceFunctions()
        fw = FwyxqkFunctions()
        step_list = []
        for a in self.task_step:
            for b in self.task_step_param:
                if a['up'] == b['task'] and a['no'] == b['step']:
                    for c in self.func:
                        if str(c['id']) == b['func']:
                            for d in self.func_type:
                                if d['id'] == c['type_id']:
                                    b['func_type'] = d['code']
                            b['step_name'] = a['name']
                            b['func'] = c['code']
                            b['func_id'] = c['id']
                            step_list.append(b)
        # print(step_list)
        # 执行
        for i in step_list:
            if len(i['value']):
                eval_text = i['func_type'] + '.' + i['func'] + '('
                value = ast.literal_eval(i['value'])
                eval_text2 = ''
                for k, v in value.items():
                    if v == '@recv':
                        value[k] = "self.recv['@recv']"
                    for a in self.task_variable:
                        if a['code'] == value[k]:
                            value[k] = a['value']
                        elif a['code'] in value[k]:
                            value[k] = value[k].replace(a['code'], a['value'])
                # print(value)
                for x, y in value.items():
                    if y == "self.recv['@recv']":
                        eval_text2 += str(x) + "=self.recv['@recv'],"
                    else:
                        eval_text2 += str(x) + "='" + str(y) + "',"
                eval_text = eval_text + eval_text2[:-1] + ')'
            else:
                eval_text = i['func_type'] + '.' + i['func'] + '()'
            logger.info('执行步骤 ' + str(i['step']) + ' ' + i['step_name'] + ' ' + eval_text)
            try:
                result = eval(eval_text)
                if str(result) == 'False':
                    logger.error('步骤 ' + str(i['step']) + ' 失败！')
                    break  # 遇到失败，直接退出任务，后面的不执行
                elif str(result) != 'True':
                    self.recv['@recv'] = result  # 获取某些函数返回的文本对象
                    logger.debug(result)
                    self.inspector(result, i['func_id'], self.task_id, i['step'])
            except Exception as e:
                logger.exception(e)
                break
        logger.info('任务 ' + str(self.task_id) + ' 执行完毕！')
        print('任务 ' + str(self.task_id) + ' 执行完毕！')
        # self.inspector('', 40, self.task_id, 1)

    # 检查是否触发策略
    def inspector(self, recv, func_id, task_id, step_id):
        # recv = [{'free': '0', 'pri': 'false', 'threads': '32', 'name': 'MONITOR', 'freethreads': '2', 'max': '65535'},
        #         {'free': '0', 'pri': 'false', 'threads': '32', 'name': 'CONSOLE', 'freethreads': '32', 'max': '65535'},
        #         {'free': '0', 'pri': 'false', 'threads': '8', 'name': '_system', 'freethreads': '7', 'max': '16'},
        #         {'free': '0', 'pri': 'false', 'threads': '32', 'name': 'BPM', 'freethreads': '8', 'max': '65535'},
        #         {'free': '0', 'pri': 'false', 'threads': '64', 'name': 'Common', 'freethreads': '64', 'max': '65535'},
        #         {'free': '0', 'pri': 'false', 'threads': '64', 'name': 'JMSCommon', 'freethreads': '54', 'max': '65535'}]
        policy = []
        for i in self.func_policy:
            if i['func_id'] == func_id:
                policy.append([i['level'], i['func_id'], i['col'], i['content'], i['ret'], i['type'], i['id']])
        policy = sorted(policy)

        for x in recv:
            # print(x)
            result = []
            for y in policy:
                text = 'y[3]'
                text2 = 'y[4]'
                for k, v in x.items():
                    text += '.replace("$' + k + '$","' + v + '")'
                    text2 += '.replace("$' + k + '$","' + v + '")'
                content = eval(text)
                ret = eval(text2)
                # print(y)
                if eval(content):
                    # [策略等级,函数id,时间,告警内容,任务id,步骤id]
                    result.append([y[0], y[1], time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), ret, task_id, step_id, y[6]])
            if len(result):
                result = min(result)
                # print(result)
                q.put(result)  # 把触发的异常告警信息放入优先进出队列中

    # 翻译特殊代码
    def translate(self, variable):
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


class ReadLog(Thread):

    def __init__(self, parent=None):
        super(ReadLog, self).__init__(parent)

    def run(self):
        if not os.path.exists('logs/system.log'):
            time.sleep(1)
        with open('logs/system.log', encoding='utf-8') as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    return line.strip().encode('utf-8')
                time.sleep(0.5)
