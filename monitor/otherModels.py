# -*- coding:utf-8 -*-
from django.db import models


# 服务运行情况涉及表
class fwyxqk(models.Model):
    begin_date = models.CharField('开始日期', max_length=10)
    end_date = models.CharField('结束日期', max_length=10)
    domain_name = models.CharField('服务域', max_length=256)
    service_code = models.CharField('服务UUID', max_length=256)
    service_name = models.CharField('服务名称', max_length=256)
    service_provider = models.CharField('服务提供者', max_length=256)
    service_consumer = models.CharField('服务消费者', max_length=256, blank=True, null=True)
    zcs = models.IntegerField('总调用数', blank=True, null=True)
    cgs = models.IntegerField('成功数', blank=True, null=True)
    sbs = models.IntegerField('失败数', blank=True, null=True)
    cgl = models.FloatField('成功率', blank=True, null=True)
    pjxysj = models.FloatField('平均响应时间', blank=True, null=True)
    zdxysj = models.FloatField('最大响应时间', blank=True, null=True)
    zxxysj = models.FloatField('最小响应时间', blank=True, null=True)
    cwxx = models.TextField('错误信息', blank=True, null=True)

    class Meta:
        verbose_name = '服务运行情况明细'
        verbose_name_plural = '服务运行情况明细'


class fwyxqk_sort(models.Model):
    type = models.CharField('服务类型', max_length=2,
                            choices=(('1', 'JMS监听服务'), ('2', '业务协同考核'), ('3', '集中认证服务'), ('4', '异常TOP20'), ('5', '高频调用服务')))
    begin_date = models.CharField('开始日期', max_length=10)
    end_date = models.CharField('结束日期', max_length=10)
    no = models.IntegerField('编号')
    service_code = models.CharField('服务UUID', max_length=256)
    service_name = models.CharField('服务名称', max_length=256)
    dyl = models.IntegerField('调用量', default=0)
    ycs = models.IntegerField('异常数', default=0)
    zyyc = models.TextField('主要异常')

    class Meta:
        verbose_name = '业务协同考核服务运行情况'
        verbose_name_plural = '业务协同考核服务运行情况'
