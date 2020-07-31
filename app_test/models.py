from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models.deletion import SET_NULL
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from api_test.models import Project
from api_test.globals import *


class WsClient(models.Model):
    """
    连接websocket的客户端
    """
    client_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='名称')
    os_type = models.CharField(max_length=16, default='darwin', verbose_name='系统类型')  # mac windows
    hubPort = models.CharField(max_length=8, default='4444', verbose_name='port')
    hubHost = models.CharField(max_length=24, default='127.0.0.1', verbose_name='host')
    isalive = models.BooleanField(default=False, verbose_name='是否可用')
    isrunning = models.BooleanField(default=False, verbose_name='是否正在运行')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    @property
    def name(self):
        return self.client_name

    def __unicode__(self):
        return self.client_name

    def __str__(self):
        return self.client_name

    class Meta:
        ordering = ("-id",)
        verbose_name = verbose_name_plural = 'WS客户端'


class DeviceVersion(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True, verbose_name='名称')
    os_type = models.CharField(max_length=16, choices=OS_TYPES, verbose_name='系统类型')  # ios, android
    version = models.CharField(max_length=16, verbose_name='版本号')    # 5.1, 6.0, 7.0
    desc = models.CharField(max_length=120, default='', verbose_name='描述')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-id",)
        verbose_name = verbose_name_plural = '系统版本'


DEVICE_STATUS_TYPES = (
    ('connected', '连接成功'),
    ('not_connected', '未连接'),
    ('error', '异常')
)


class Device(models.Model):
    """
    添加的手机测试设备，每个人只显示自己添加的设置
    """
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name='设备名')
    alias = models.CharField(max_length=64, null=True, blank=True, verbose_name='昵称')
    os_type = models.CharField(max_length=16, choices=OS_TYPES, verbose_name='系统类型')  # ios, android
    version = models.ForeignKey(DeviceVersion, verbose_name='版本', on_delete=SET_NULL, null=True)
    status = models.CharField(max_length=20, null=True, blank=True, verbose_name='设备状态',
                              choices=DEVICE_STATUS_TYPES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name="创建人", related_name="device_create_user")
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    @property
    def version_name(self):
        return '%s-%s' % (self.version.os_type, self.version.version)

    @property
    def current_status(self):
        return dict(DEVICE_STATUS_TYPES).get(self.status)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-id",)
        verbose_name = verbose_name_plural = '设备'


class ScriptTmpl(models.Model):
    """
    自动生成测试脚本时的模板
    """
    name = models.CharField(max_length=20, verbose_name='模板名称')
    content = models.TextField(default='', verbose_name='模板内容')
    desc = models.CharField(max_length=200, default='', verbose_name='描述')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-id",)
        verbose_name = '脚本模板'
        verbose_name_plural = '脚本模板'


class ScriptGroupLevelFirst(models.Model):
    """
    一级分组
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='一级分组名称')

    @property
    def project_name(self):
        return self.project.name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-id",)
        verbose_name = verbose_name_plural = 'app用例分组'


Script_STATUS_TYPES = (
    ('start', '开启'),
    ('run', '运行中'),
    ('end', '完成'),
    ('error', '异常')
)


class Script(models.Model):
    name = models.CharField(max_length=20, null=True, verbose_name='名称')
    project = models.ForeignKey(Project, related_name='script_project',
                                on_delete=models.CASCADE, verbose_name='所属项目')
    scriptGroupLevelFirst = models.ForeignKey(ScriptGroupLevelFirst,
                                               blank=True, null=True,
                                               related_name='First',
                                               on_delete=models.SET_NULL,
                                               verbose_name='所属一级分组')
    content = models.TextField(verbose_name='内容', default='', null=True)
    # status = models.BooleanField(default=True, verbose_name='状态')
    status = models.CharField(max_length=16, default='end', choices=Script_STATUS_TYPES,
                              verbose_name='运行状态')
    # 真实的运行状态应该放在相应的automationScript的类中，这样不影响其它人的状态
    mockStatus = models.BooleanField(default=False, verbose_name="mock状态")

    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    @property
    def short_content(self):
        if len(self.content) <= 10:
            return self.content
        else:
            return self.content[:10] + '...'

    @property
    def project_name(self):
        if self.project:
            return self.project.name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-id",)
        verbose_name = verbose_name_plural = 'Appium脚本'  # App测试用例


# 用于真实测试
class AutomationGroupLevelFirst(models.Model):
    """
    自动化用例一级分组
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                verbose_name='项目',
                                related_name='script_automation_group_project')
    name = models.CharField(max_length=50, verbose_name='用例一级分组')

    @property
    def project_name(self):
        return self.project.name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-id",)
        verbose_name = '用例分组'
        verbose_name_plural = '用例分组管理'


class AutomationTestScript(models.Model):
    """
    自动化测试用例
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project,
                                related_name='automation_testcase_project',
                                on_delete=models.CASCADE,
                                verbose_name='所属项目')
    automationGroupLevelFirst = models.ForeignKey(AutomationGroupLevelFirst, blank=True, null=True,
                                                  on_delete=models.SET_NULL, verbose_name='所属用例一级分组',
                                                  related_name="auto_test_script_automationGroupLevelFirst")
    # automationGroupLevelSecond = models.ForeignKey(AutomationGroupLevelSecond, blank=True, null=True,
    #                                                on_delete=models.SET_NULL, verbose_name='所属用例二级分组')
    caseName = models.CharField(max_length=50, verbose_name='用例名称')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name="创建人", related_name="apptestcase_createUser1")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间',
                                      blank=True)

    @property
    def project_name(self):
        return self.project.name

    def __unicode__(self):
        return self.caseName

    def __str__(self):
        return self.caseName

    class Meta:
        ordering = ("-id",)
        verbose_name = '自动化测试用例'
        verbose_name_plural = '自动化测试用例'


class AutomationTestAppCase(models.Model):
    """
    自动化测试用例(app)
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目',
                                related_name='automation_test_appcase_project')
    automationGroupLevelFirst = models.ForeignKey(AutomationGroupLevelFirst, blank=True, null=True,
                                                  on_delete=models.SET_NULL, verbose_name='所属用例一级分组',
                                                  related_name="automation_test_auto_group")
    caseName = models.CharField(max_length=50, verbose_name='用例名称')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name="创建人", related_name="automation_test_create_user")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.caseName

    def __str__(self):
        return self.caseName

    class Meta:
        ordering = ("-id",)
        verbose_name = '自动化测试用例'
        verbose_name_plural = '自动化测试用例'


class AutomationCaseScript(models.Model):
    """
    用例执行脚本，每个用户添加脚本形成一个caseScript记录
    """
    id = models.AutoField(primary_key=True)
    automationTestCase = models.ForeignKey(AutomationTestAppCase, on_delete=models.CASCADE,
                                           verbose_name='用例', related_name="auto_case_script_testcase")
    name = models.CharField(max_length=50, verbose_name='脚本名称')
    httpType = models.CharField(max_length=50, default='HTTP', verbose_name='HTTP/HTTPS', choices=HTTP_CHOICE)
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    requestParameterType = models.CharField(max_length=50, verbose_name='参数请求格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    formatRaw = models.BooleanField(default=False, verbose_name="是否转换成源数据")
    examineType = models.CharField(default='no_check', max_length=50, verbose_name='校验方式', choices=EXAMINE_TYPE_CHOICE)
    httpCode = models.CharField(max_length=50, blank=True, null=True, verbose_name='HTTP状态', choices=HTTP_CODE_CHOICE)
    responseData = models.TextField(blank=True, null=True, verbose_name='返回内容')
    desc = models.CharField(max_length=200, blank=True, null=True, verbose_name='描述',
                            default='无描述')

    # =========从Script中复制 ===========
    content = models.TextField(verbose_name='内容', default='', null=True)
    status = models.CharField(max_length=16, default='end', choices=Script_STATUS_TYPES,
                              verbose_name='运行状态')
    tmpl = models.ForeignKey(ScriptTmpl, default=None, null=True,
                             on_delete=models.SET_NULL, verbose_name='使用的模板')
    device = models.ForeignKey(Device, default=None, null=True,
                              on_delete=models.SET_NULL, verbose_name='运行的设备')
    # 真实的运行状态应该放在相应的automationScript的类中，这样不影响其它人的状态
    mockStatus = models.BooleanField(default=False, verbose_name="mock状态")
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-id",)
        verbose_name = '用例脚本'
        verbose_name_plural = '用例脚本管理'


class AutomationParameter(models.Model):
    """
    用例执行需要的参数
    """
    id = models.AutoField(primary_key=True)
    # automationCaseApi = models.ForeignKey(AutomationCaseApi, related_name='parameterList',
    #                                       on_delete=models.CASCADE, verbose_name='接口')
    # automationCaseApi
    automationCaseScript = models.ForeignKey(AutomationCaseScript, related_name='parameterList',
                                             on_delete=models.CASCADE, verbose_name='用例')
    name = models.CharField(max_length=1024, verbose_name='参数名')
    value = models.CharField(max_length=1024, verbose_name='内容', blank=True, null=True)
    interrelate = models.BooleanField(default=False, verbose_name='是否关联')

    def __unicode__(self):
        return self.value

    class Meta:
        ordering = ("-id",)
        verbose_name = '用例参数'
        verbose_name_plural = '用例参数管理'


class AutomationTestResultApp(models.Model):
    """
    手动执行结果
    """
    id = models.AutoField(primary_key=True)
    automationCaseScript = models.OneToOneField(AutomationCaseScript, on_delete=models.CASCADE,
                                                verbose_name='脚本', related_name="test_result")
    url = models.CharField(max_length=1024, verbose_name='请求地址')
    requestType = models.CharField(max_length=1024, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    host = models.CharField(max_length=1024, verbose_name='测试地址', null=True, blank=True)
    header = models.CharField(max_length=1024, blank=True, null=True, verbose_name='请求头')
    parameter = models.TextField(blank=True, null=True, verbose_name='请求参数')
    statusCode = models.CharField(blank=True, null=True, max_length=1024, verbose_name='期望HTTP状态',
                                  choices=HTTP_CODE_CHOICE)
    examineType = models.CharField(max_length=1024, verbose_name='匹配规则')
    data = models.TextField(blank=True, null=True, verbose_name='规则内容')
    httpStatus = models.CharField(max_length=50, blank=True, null=True, verbose_name='http状态', choices=HTTP_CODE_CHOICE)
    responseData = models.TextField(blank=True, null=True, verbose_name='实际返回内容')
    testTime = models.DateTimeField(auto_now_add=True, verbose_name='测试时间')

    result = models.CharField(max_length=50, verbose_name='测试结果', choices=RESULT_CHOICE)
    cmd = models.CharField(max_length=1024, null=True, default='', verbose_name='执行命令')
    out = models.TextField(blank=True, null=True, default='', verbose_name='打印结果')
    err = models.TextField(blank=True, null=True, default='', verbose_name='输出异常')

    def __unicode__(self):
        return str(self.id) + ' ' + self.result

    class Meta:
        ordering = ("-id",)
        verbose_name = '手动测试结果'
        verbose_name_plural = '手动测试结果管理'




