from django.http import HttpResponse
from django.shortcuts import render_to_response
from monitor.util import preload
from django.core.cache import cache
from monitor.util import getResource as rs
from dwebsocket.decorators import accept_websocket
import os, time

preload.loading()


@accept_websocket
def echo_log(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return HttpResponse('error')
    else:
        if not os.path.exists('logs/system.log'):
            time.sleep(1)
        with open('logs/system.log', encoding='utf-8') as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    request.websocket.send(line.strip().encode('utf-8'))
                    time.sleep(0.1)


def sms_send(request):
    from monitor.alarm.sms import SMS
    SMS().send_sms(
        **{'time': '2018/05/27 18:27:42', 'alarmlevel': '01', 'alarmid': 'A3', 'maindata': 'AlarmID=A3', 'alarmcontent': '总线 BPM 通道使用率大于70%，警告！', 'ipaddress': '',
           'alarmcount': '3',
           'firsttime': '2018/05/27 18:27:01', 'alarmstatus': '01', 'policy': 'S3-12-1', 'areacode': '0300', 'alarmtype': '01', 'originalid': 'S3-12-1', 'alarmcate': '08',
           'endtime': '2018/05/27 18:27:41'})
    return HttpResponse(1)


def task_start(request):
    task_no = request.POST.get('no')
    result = rs.task_start(task_no)
    return HttpResponse(result)


def functions(request):
    pass


def deletetable(request):
    code = request.GET.get('code')  # 获取sysmenu表的code值
    data = request.body.decode()
    status = rs.del_tabledata(code, data)
    return HttpResponse(status)


def updatetable(request):
    code = request.GET.get('code')  # 获取sysmenu表的code值
    data = request.body.decode()  # 获取要修改的数据内容，获取页面传到后台的json数据要用request.body.decode()
    # print(code, data)
    status = rs.set_tabledata(code, data)
    return HttpResponse(status)


def tabledata(request):
    code = request.GET.get('code')  # 必须字段
    code_dict = rs.get_menutitle(code)
    # print(code_dict)
    page = request.POST.get('page')
    limit = request.POST.get('limit')
    if code_dict['type'] == '1':
        condition = request.POST.get('condition', '')  # 条件，也可以作为搜索条件
        columns = request.POST.get('columns', '')  # 关键字搜索的字段逗号分隔
        keyword = request.POST.get('keyword', '')  # 关键字
        table_data = rs.get_tabledata(code_dict['table'], page, limit, condition, columns, keyword, code_dict['code_class'])
        return HttpResponse(table_data)
    elif code_dict['type'] == '2':
        param_dict = request.POST.get('param')  # 必要条件
        # print(param_dict)
        table_data = rs.get_tabledata_sql(page, limit, code_dict['table'], param_dict, code_dict['code_class'])
        return HttpResponse(table_data)


def manager(request):
    code = request.GET.get('code')
    code_dict = rs.get_menutitle(code)
    menu_name = code_dict['code_name']
    up_menu_name = rs.get_menutitle_up(code)
    return render_to_response(code_dict['file_path'], {'menu_name': menu_name, 'up_menu_name': up_menu_name})


def login(request):
    return render_to_response('login.html')


def index(request):
    return render_to_response('index.html', {'menutitle': '信息集成平台管理工具', 'leftmenu': cache.get('leftmenu')})


def welcome(request):
    return render_to_response('welcome.html')
