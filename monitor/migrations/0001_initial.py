# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-29 09:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Functions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256, verbose_name='代码')),
                ('name', models.CharField(max_length=256, verbose_name='名称')),
                ('param', models.CharField(blank=True, max_length=1000, null=True, verbose_name='参数')),
                ('ret', models.CharField(blank=True, max_length=256, null=True, verbose_name='返回值')),
                ('remark', models.CharField(blank=True, max_length=1000, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '系统函数表',
                'verbose_name': '系统函数表',
            },
        ),
        migrations.CreateModel(
            name='FunctionsParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256, verbose_name='参数代码')),
                ('name', models.CharField(max_length=256, verbose_name='参数名称')),
                ('defaults', models.CharField(blank=True, max_length=256, null=True, verbose_name='参数默认值')),
                ('remark', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Functions', verbose_name='所属函数编号')),
            ],
            options={
                'verbose_name_plural': '系统函数参数表',
                'verbose_name': '系统函数参数表',
            },
        ),
        migrations.CreateModel(
            name='FunctionsPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('1', '文本型'), ('2', '字典型'), ('3', '列表型'), ('4', '列表字典型')], max_length=1, verbose_name='策略监控类型')),
                ('col', models.CharField(blank=True, max_length=256, null=True, verbose_name='字段')),
                ('content', models.TextField(verbose_name='策略内容')),
                ('level', models.IntegerField(choices=[(1, '紧急'), (2, '重大'), (3, '一般'), (4, '提示'), (5, '其他')], verbose_name='异常等级')),
                ('ret', models.CharField(blank=True, max_length=256, null=True, verbose_name='触发策略返回文本')),
                ('func', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Functions', verbose_name='关联函数')),
            ],
            options={
                'verbose_name_plural': '系统函数关联策略表',
                'verbose_name': '系统函数关联策略表',
            },
        ),
        migrations.CreateModel(
            name='FunctionsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256, verbose_name='代码')),
                ('name', models.CharField(max_length=256, verbose_name='名称')),
            ],
            options={
                'verbose_name_plural': '系统函数类型表',
                'verbose_name': '系统函数类型表',
            },
        ),
        migrations.CreateModel(
            name='fwyxqk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.CharField(max_length=8, verbose_name='开始日期')),
                ('end_date', models.CharField(max_length=8, verbose_name='结束日期')),
                ('domain_name', models.CharField(max_length=256, verbose_name='服务域')),
                ('service_code', models.CharField(max_length=256, verbose_name='服务UUID')),
                ('service_name', models.CharField(max_length=256, verbose_name='服务名称')),
                ('service_provider', models.CharField(max_length=256, verbose_name='服务提供者')),
                ('service_consumer', models.CharField(blank=True, max_length=256, null=True, verbose_name='服务消费者')),
                ('zcs', models.IntegerField(blank=True, null=True, verbose_name='总调用数')),
                ('cgs', models.IntegerField(blank=True, null=True, verbose_name='成功数')),
                ('sbs', models.IntegerField(blank=True, null=True, verbose_name='失败数')),
                ('cgl', models.FloatField(blank=True, null=True, verbose_name='成功率')),
                ('pjxysj', models.FloatField(blank=True, null=True, verbose_name='平均响应时间')),
                ('zdxysj', models.FloatField(blank=True, null=True, verbose_name='最大响应时间')),
                ('zxxysj', models.FloatField(blank=True, null=True, verbose_name='最小响应时间')),
                ('cwxx', models.TextField(blank=True, null=True, verbose_name='错误信息')),
            ],
            options={
                'verbose_name_plural': '服务运行情况明细',
                'verbose_name': '服务运行情况明细',
            },
        ),
        migrations.CreateModel(
            name='fwyxqk_sort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('1', 'JMS监听服务'), ('2', '业务协同考核'), ('3', '集中认证服务'), ('4', '异常TOP20'), ('5', '高频调用服务')], max_length=2, verbose_name='服务类型')),
                ('begin_date', models.CharField(max_length=8, verbose_name='开始日期')),
                ('end_date', models.CharField(max_length=8, verbose_name='结束日期')),
                ('no', models.IntegerField(verbose_name='编号')),
                ('service_code', models.CharField(max_length=256, verbose_name='服务UUID')),
                ('service_name', models.CharField(max_length=256, verbose_name='服务名称')),
                ('dyl', models.IntegerField(default=0, verbose_name='调用量')),
                ('ycs', models.IntegerField(default=0, verbose_name='异常数')),
                ('zyyc', models.TextField(verbose_name='主要异常')),
            ],
            options={
                'verbose_name_plural': '业务协同考核服务运行情况',
                'verbose_name': '业务协同考核服务运行情况',
            },
        ),
        migrations.CreateModel(
            name='PolicyLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('func_id', models.IntegerField(verbose_name='关联函数ID')),
                ('task_id', models.IntegerField(verbose_name='关联任务ID')),
                ('step_id', models.IntegerField(verbose_name='关联步骤ID')),
                ('alarmlevel', models.CharField(max_length=2, verbose_name='告警级别')),
                ('alarmtime', models.DateTimeField(verbose_name='告警时间')),
                ('alarmcontent', models.TextField(verbose_name='告警内容')),
                ('ipaddress', models.CharField(blank=True, max_length=30, null=True, verbose_name='告警IP地址')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.FunctionsPolicy', verbose_name='配置项ID')),
            ],
            options={
                'verbose_name_plural': '策略告警日志表',
                'verbose_name': '策略告警日志表',
            },
        ),
        migrations.CreateModel(
            name='SMSLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', models.CharField(max_length=30, verbose_name='配置项编码')),
                ('originalid', models.CharField(blank=True, max_length=100, null=True, verbose_name='系统资源ID')),
                ('maindata', models.CharField(max_length=100, verbose_name='告警主数据')),
                ('alarmid', models.CharField(max_length=100, verbose_name='告警ID')),
                ('alarmlevel', models.CharField(max_length=2, verbose_name='告警级别')),
                ('alarmcontent', models.TextField(verbose_name='告警内容')),
                ('alarmcount', models.IntegerField(verbose_name='重复次数')),
                ('alarmcate', models.CharField(blank=True, max_length=2, null=True, verbose_name='告警分类')),
                ('alarmtype', models.CharField(blank=True, max_length=2, null=True, verbose_name='告警类型')),
                ('alarmstatus', models.CharField(blank=True, max_length=2, null=True, verbose_name='告警处理状态')),
                ('areacode', models.CharField(max_length=10, verbose_name='单位编码')),
                ('ipaddress', models.CharField(blank=True, max_length=30, null=True, verbose_name='告警IP地址')),
                ('time', models.DateTimeField(verbose_name='消息发送时间')),
                ('firsttime', models.DateTimeField(verbose_name='首次产生告警时间')),
                ('endtime', models.DateTimeField(verbose_name='最后一次产生告警时间')),
            ],
            options={
                'verbose_name_plural': '短信发送日志表',
                'verbose_name': '短信发送日志表',
            },
        ),
        migrations.CreateModel(
            name='SysMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.CharField(max_length=64, verbose_name='所属表')),
                ('field', models.CharField(max_length=64, verbose_name='字段')),
                ('code', models.CharField(max_length=64, verbose_name='参数')),
            ],
            options={
                'verbose_name_plural': '字段代码对应表',
                'verbose_name': '字段代码对应表',
            },
        ),
        migrations.CreateModel(
            name='SysMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='代码')),
                ('code_name', models.CharField(max_length=256, verbose_name='代码名称')),
                ('code_class', models.CharField(blank=True, max_length=64, null=True, verbose_name='菜单class代码')),
                ('up_code', models.IntegerField(verbose_name='上级代码')),
                ('url', models.CharField(blank=True, max_length=256, null=True, verbose_name='路由路径')),
                ('file_path', models.CharField(blank=True, max_length=256, null=True, verbose_name='页面路径')),
                ('table', models.CharField(blank=True, max_length=256, null=True, verbose_name='所属表')),
                ('icon', models.CharField(blank=True, max_length=256, null=True, verbose_name='图标')),
                ('type', models.CharField(max_length=2, verbose_name='类型')),
                ('remark', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '系统菜单表',
                'verbose_name': '系统菜单表',
            },
        ),
        migrations.CreateModel(
            name='SysParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, verbose_name='代码')),
                ('code_name', models.CharField(max_length=256, verbose_name='代码名称')),
                ('param', models.CharField(max_length=64, verbose_name='参数')),
                ('param_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='参数名称')),
                ('flag', models.IntegerField(choices=[(1, '启用'), (0, '停用')], default=1, verbose_name='启用标志')),
                ('memo', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '系统代码表',
                'verbose_name': '系统代码表',
            },
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.IntegerField(verbose_name='编号')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='名称')),
                ('content', models.CharField(blank=True, max_length=256, null=True, verbose_name='操作内容')),
                ('type', models.CharField(choices=[('1', '任务'), ('2', '步骤')], max_length=1, verbose_name='类型')),
                ('up', models.IntegerField(verbose_name='所属任务编号')),
                ('param', models.CharField(blank=True, max_length=256, null=True, verbose_name='自定义参数')),
                ('ploy', models.CharField(blank=True, choices=[('1', '秒'), ('2', '分钟'), ('3', '小时'), ('4', '天'), ('5', '周'), ('6', '周一'), ('7', '周二'), ('8', '周三'), ('9', '周四'), ('10', '周五'), ('11', '周六'), ('12', '周日')], max_length=2, null=True, verbose_name='定时策略')),
                ('time_set', models.CharField(blank=True, max_length=10, null=True, verbose_name='时间设置')),
                ('remark', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '任务列表',
                'verbose_name': '任务列表',
            },
        ),
        migrations.CreateModel(
            name='TaskListConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.IntegerField(verbose_name='所属任务')),
                ('step', models.IntegerField(verbose_name='所属步骤')),
                ('func', models.CharField(max_length=20, verbose_name='函数编号')),
                ('value', models.CharField(blank=True, max_length=256, null=True, verbose_name='参数内容')),
            ],
            options={
                'verbose_name_plural': '任务列表参数配置表',
                'verbose_name': '任务列表参数配置表',
            },
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.IntegerField(verbose_name='所属任务')),
                ('log_time', models.DateTimeField(auto_now_add=True, verbose_name='日志时间')),
                ('log', models.TextField(blank=True, null=True, verbose_name='日志内容')),
            ],
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, verbose_name='代码')),
                ('name', models.CharField(max_length=256, verbose_name='代码名称')),
                ('value', models.CharField(blank=True, max_length=256, null=True, verbose_name='代码值')),
                ('type', models.CharField(choices=[('1', '系统变量'), ('2', '任务变量')], default='1', max_length=2, verbose_name='类型')),
                ('task', models.IntegerField(default=-1, verbose_name='所属任务')),
            ],
            options={
                'verbose_name_plural': '系统变量表',
                'verbose_name': '系统变量表',
            },
        ),
        migrations.AlterUniqueTogether(
            name='tasklistconfig',
            unique_together=set([('task', 'step')]),
        ),
        migrations.AlterUniqueTogether(
            name='sysparam',
            unique_together=set([('code', 'param')]),
        ),
        migrations.AlterUniqueTogether(
            name='sysmenu',
            unique_together=set([('code', 'up_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='sysmapping',
            unique_together=set([('table', 'field')]),
        ),
        migrations.AddField(
            model_name='functions',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.FunctionsType', verbose_name='类别'),
        ),
    ]
