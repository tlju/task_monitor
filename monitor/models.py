from django.db import models


# Create your models here.
class SysMenu(models.Model):
    code = models.IntegerField('代码')
    code_name = models.CharField('代码名称', max_length=256)
    code_class = models.CharField('菜单class代码', max_length=64, blank=True, null=True)
    up_code = models.IntegerField('上级代码')
    url = models.CharField('路由路径', max_length=256, blank=True, null=True)
    file_path = models.CharField('页面路径', max_length=256, blank=True, null=True)
    table = models.CharField('所属表', max_length=256, blank=True, null=True)
    icon = models.CharField('图标', max_length=256, blank=True, null=True)
    type = models.CharField('类型', max_length=2)
    status = models.CharField('状态', max_length=2, choices=(('1', '在用'), ('2', '停用')), default='1')
    remark = models.CharField('备注', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '系统菜单表'
        verbose_name_plural = '系统菜单表'
        unique_together = ('code', 'up_code')


class Functions(models.Model):
    type = models.ForeignKey('FunctionsType', verbose_name='类别')
    code = models.CharField('代码', max_length=256)
    name = models.CharField('名称', max_length=256)
    param = models.CharField('参数', max_length=1000, blank=True, null=True)
    ret = models.CharField('返回值', max_length=256, blank=True, null=True)
    status = models.CharField('状态', max_length=1, choices=(('1', '使用中'), ('2', '停用')), default='1')
    remark = models.CharField('备注', max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = '系统函数表'
        verbose_name_plural = '系统函数表'

    def __str__(self):
        return self.name


class FunctionsType(models.Model):
    code = models.CharField('代码', max_length=256)
    name = models.CharField('名称', max_length=256)
    value = models.CharField('代码函数', max_length=256)

    class Meta:
        verbose_name = '系统函数类型表'
        verbose_name_plural = '系统函数类型表'

    def __str__(self):
        return self.name


class FunctionsParam(models.Model):
    no = models.ForeignKey('Functions', verbose_name='所属函数编号')
    code = models.CharField('参数代码', max_length=256)
    name = models.CharField('参数名称', max_length=256)
    defaults = models.CharField('参数默认值', max_length=256, blank=True, null=True)
    remark = models.CharField('备注', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '系统函数参数表'
        verbose_name_plural = '系统函数参数表'

    def __str__(self):
        return self.name + ' ' + self.code + ' ' + self.defaults


class FunctionsPolicy(models.Model):
    func = models.ForeignKey('Functions', verbose_name='关联函数')
    type = models.CharField('策略监控类型', max_length=1, choices=(('1', '文本型'), ('2', '字典型'), ('3', '列表型'), ('4', '列表字典型')))
    col = models.CharField('字段', max_length=256, null=True, blank=True)  # 字典的key 或 列表的下标 或 文本的内容，用“,”分隔
    content = models.TextField('策略内容')  # 策略关键字段 前后加“$”，根据传来的字典的key来替换处理
    level = models.IntegerField('异常等级', choices=((1, '紧急'), (2, '重大'), (3, '一般'), (4, '提示'), (5, '其他')))  # 1级最高
    ret = models.CharField('触发策略返回文本', max_length=256, null=True, blank=True)  # 可作为触发的短信告警内容

    class Meta:
        verbose_name = '系统函数关联策略表'
        verbose_name_plural = '系统函数关联策略表'


class TaskList(models.Model):
    no = models.IntegerField('编号')
    name = models.CharField('名称', max_length=256, blank=True, null=True)
    content = models.CharField('操作内容', max_length=256, blank=True, null=True)
    type = models.CharField('类型', max_length=1, choices=(('1', '任务'), ('2', '步骤'), ('3', '批量任务'), ('4', '循环任务'), ('5', '子任务')))
    up = models.IntegerField('所属任务编号')
    param = models.CharField('自定义参数', max_length=5000, blank=True, null=True)
    ploy = models.CharField('定时策略', max_length=2, blank=True, null=True, choices=(('1', '秒'), ('2', '分钟'), ('3', '小时'), ('4', '天'),
                                                                                  ('5', '周'), ('6', '周一'), ('7', '周二'), ('8', '周三')
                                                                                  , ('9', '周四'), ('10', '周五'), ('11', '周六'), ('12', '周日')))
    time_set = models.CharField('时间设置', max_length=10, blank=True, null=True)
    remark = models.CharField('备注', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '任务列表'
        verbose_name_plural = '任务列表'
        unique_together = ('no', 'type', 'up')


class TaskListConfig(models.Model):
    task = models.IntegerField('所属任务')
    step = models.IntegerField('所属步骤')
    func = models.CharField('函数编号', max_length=20)
    value = models.CharField('参数内容', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '任务列表参数配置表'
        verbose_name_plural = '任务列表参数配置表'
        unique_together = ('task', 'step')


class TaskLog(models.Model):
    task = models.IntegerField('所属任务')
    log_time = models.DateTimeField('日志时间', blank=True, auto_now_add=True)
    log = models.TextField('日志内容', blank=True, null=True)
    variable = models.TextField('任务参数内容', blank=True, null=True)
    status = models.IntegerField('状态', choices=((1, '成功'), (2, '失败')))


class SysMapping(models.Model):
    table = models.CharField('所属表', max_length=64)
    field = models.CharField('字段', max_length=64)
    code = models.CharField('参数', max_length=64)

    class Meta:
        verbose_name = '字段代码对应表'
        verbose_name_plural = '字段代码对应表'
        unique_together = ('table', 'field')


class SysParam(models.Model):
    code = models.CharField('代码', max_length=64)
    code_name = models.CharField('代码名称', max_length=256)
    param = models.CharField('参数', max_length=64)
    param_name = models.CharField('参数名称', max_length=256, null=True, blank=True)
    flag = models.IntegerField('启用标志', choices=((1, '启用'), (0, '停用')), default=1)
    memo = models.CharField('备注', max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = '系统代码表'
        verbose_name_plural = '系统代码表'
        unique_together = ('code', 'param')


class SysSetting(models.Model):
    code = models.CharField('配置代码', max_length=64)
    code_name = models.CharField('配置名称', max_length=256)
    value = models.CharField('配置值', max_length=256, null=True, blank=True)
    flag = models.IntegerField('启用标志', choices=((1, '启用'), (0, '停用')), default=1)
    memo = models.CharField('备注', max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = '系统代码表'
        verbose_name_plural = '系统代码表'
        unique_together = ('code', 'value')


class Variable(models.Model):
    code = models.CharField('代码', max_length=64)
    name = models.CharField('代码名称', max_length=256)
    value = models.CharField('代码值', max_length=256, null=True, blank=True)
    type = models.CharField('类型', max_length=2, choices=(('1', '系统变量'), ('2', '任务变量'), ('3', '循环任务变量')))
    task = models.IntegerField('所属任务', default=-1)

    class Meta:
        verbose_name = '系统变量表'
        verbose_name_plural = '系统变量表'
        unique_together = ('id', 'code')


class PolicyLog(models.Model):
    policy = models.ForeignKey('FunctionsPolicy', verbose_name='配置项ID')
    func_id = models.IntegerField('关联函数ID')
    task_id = models.IntegerField('关联任务ID')
    step_id = models.IntegerField('关联步骤ID')
    alarmlevel = models.CharField('告警级别', max_length=2)
    alarmtime = models.DateTimeField('告警时间')
    alarmcontent = models.TextField('告警内容')
    ipaddress = models.CharField('告警IP地址', max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = '策略告警日志表'
        verbose_name_plural = '策略告警日志表'

    def __str__(self):
        return str(self.id) + str(self.func_id)


class SMSLog(models.Model):
    policy = models.CharField('配置项编码', max_length=30)
    originalid = models.CharField('系统资源ID', max_length=100, blank=True, null=True)
    maindata = models.CharField('告警主数据', max_length=100)
    alarmid = models.CharField('告警ID', max_length=100)
    alarmlevel = models.CharField('告警级别', max_length=2)
    alarmcontent = models.TextField('告警内容')
    alarmcount = models.IntegerField('重复次数')
    alarmcate = models.CharField('告警分类', max_length=2, blank=True, null=True)
    alarmtype = models.CharField('告警类型', max_length=2, blank=True, null=True)
    alarmstatus = models.CharField('告警处理状态', max_length=2, blank=True, null=True)
    areacode = models.CharField('单位编码', max_length=10)
    ipaddress = models.CharField('告警IP地址', max_length=30, blank=True, null=True)
    time = models.DateTimeField('消息发送时间')
    firsttime = models.DateTimeField('首次产生告警时间')
    endtime = models.DateTimeField('最后产生告警时间')

    class Meta:
        verbose_name = '短信发送日志表'
        verbose_name_plural = '短信发送日志表'


# 用户表 包含所有用户
class UserProfile(models.Model):
    name = models.CharField('名称', max_length=30)
    email = models.EmailField('邮箱')
    phone = models.CharField('联系电话', max_length=11)
    type = models.CharField('用户类型', max_length=1, choices=(('1', '普通用户'), ('2', '管理员')), default='1')
    memo = models.TextField('备注', blank=True)
    create_at = models.DateTimeField('创建时间', blank=True, auto_now_add=True)
    update_at = models.DateTimeField('修改时间', blank=True, auto_now=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.name


# 管理员信息
class AdminInfo(models.Model):
    user = models.OneToOneField('UserProfile', verbose_name='用户')
    username = models.CharField('用户名', max_length=50)
    password = models.CharField('密码', max_length=200)

    class Meta:
        verbose_name = '管理员信息'
        verbose_name_plural = '管理员信息'


class Server(models.Model):
    sn = models.CharField('SN号', max_length=64)
    model = models.CharField('系统类型', max_length=1, choices=(('1', 'linux'), ('2', 'windows')), default='1')
    host_location = models.CharField('主机位置', max_length=1, choices=(('1', '远程'), ('2', '本地')), default='1')
    username = models.CharField('登陆帐号', max_length=32, blank=True, null=True)
    password = models.CharField('密码', max_length=32, blank=True, null=True)
    ipaddress = models.GenericIPAddressField('IP地址', blank=True, null=True)
    root_path = models.CharField('根目录', max_length=256, blank=True, null=True)
    memo = models.TextField('备注', null=True, blank=True)
    create_at = models.DateTimeField('创建时间', blank=True, auto_now_add=True)
    update_at = models.DateTimeField('修改时间', blank=True, auto_now=True)
    user_profile = models.ForeignKey('UserProfile', verbose_name='设备管理员', related_name='+', null=True, blank=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'
