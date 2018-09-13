from django.contrib import admin

# Register your models here.
from monitor import models
from monitor import otherModels


class AdminSysMenu(admin.ModelAdmin):
    list_display = ('id', 'code', 'code_name', 'code_class', 'up_code', 'url', 'file_path', 'table', 'type', 'icon')
    ordering = ('id',)


class AdminSysMapping(admin.ModelAdmin):
    list_display = ('id', 'table', 'field', 'code')
    ordering = ('id',)


class AdminSysParam(admin.ModelAdmin):
    list_display = ('id', 'code', 'code_name', 'param', 'param_name', 'flag', 'memo')
    ordering = ('id',)


class AdminSysSetting(admin.ModelAdmin):
    list_display = ('id', 'code', 'code_name', 'value', 'flag', 'memo')
    ordering = ('id',)


class AdminFunctions(admin.ModelAdmin):
    list_display = ('id', 'type', 'code', 'name', 'param', 'ret', 'status', 'remark')
    ordering = ('id',)


class AdminFunctionsType(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'value')
    ordering = ('id',)


class AdminFunctionsParam(admin.ModelAdmin):
    list_display = ('id', 'no', 'code', 'name', 'defaults', 'remark')
    ordering = ('id',)


class AdminFunctionsPolicy(admin.ModelAdmin):
    list_display = ('id', 'func', 'type', 'col', 'content', 'level', 'ret')
    ordering = ('id',)


class AdminTaskList(admin.ModelAdmin):
    list_display = ('id', 'no', 'name', 'content', 'type', 'up', 'param', 'ploy', 'time_set', 'remark')
    ordering = ('id',)


class AdminTaskListConfig(admin.ModelAdmin):
    list_display = ('id', 'task', 'step', 'func', 'value')
    ordering = ('id',)


class AdminVariable(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'value', 'type', 'task')
    ordering = ('id',)


class AdminPolicyLog(admin.ModelAdmin):
    list_display = (
        'id', 'policy', 'func_id', 'task_id', 'step_id', 'alarmlevel', 'alarmtime', 'alarmcontent', 'ipaddress')
    ordering = ('id',)


class AdminSMSLog(admin.ModelAdmin):
    list_display = (
        'id', 'policy', 'originalid', 'maindata', 'alarmid', 'alarmlevel', 'alarmcontent', 'alarmcount', 'alarmcate', 'alarmtype', 'alarmstatus', 'areacode', 'ipaddress', 'time',
        'firsttime', 'endtime')
    ordering = ('id',)


class AdminUserProfile(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'type', 'memo')
    ordering = ('id',)


class AdminAdminInfo(admin.ModelAdmin):
    list_display = ('id', 'user', 'username', 'password')
    ordering = ('user_id',)


class AdminServer(admin.ModelAdmin):
    list_display = ('id', 'sn', 'model', 'host_location', 'username', 'password', 'ipaddress', 'root_path', 'memo', 'user_profile')
    ordering = ('id',)


admin.site.register(models.SysMenu, AdminSysMenu)
admin.site.register(models.SysMapping, AdminSysMapping)
admin.site.register(models.SysParam, AdminSysParam)
admin.site.register(models.SysSetting, AdminSysSetting)
admin.site.register(models.Functions, AdminFunctions)
admin.site.register(models.FunctionsType, AdminFunctionsType)
admin.site.register(models.FunctionsParam, AdminFunctionsParam)
admin.site.register(models.FunctionsPolicy, AdminFunctionsPolicy)
admin.site.register(models.TaskList, AdminTaskList)
admin.site.register(models.TaskListConfig, AdminTaskListConfig)
admin.site.register(models.Variable, AdminVariable)
admin.site.register(models.PolicyLog, AdminPolicyLog)
admin.site.register(models.SMSLog, AdminSMSLog)
admin.site.register(models.UserProfile, AdminUserProfile)
admin.site.register(models.AdminInfo, AdminAdminInfo)
admin.site.register(models.Server, AdminServer)
