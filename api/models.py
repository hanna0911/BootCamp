'''
描述数据库结构的文件
'''

from django.db import models

# Create your models here.

NAME_LEN = 50
SHORT_INFO_LEN = 20
LONG_INFO_LEN = 200


class PrivateInfo(models.Model):
    """
    user table
    """
    name = models.CharField(max_length=NAME_LEN)  # 用户的真实姓名
    city = models.CharField(max_length=SHORT_INFO_LEN)  # 用户所在城市
    dept = models.CharField(max_length=SHORT_INFO_LEN)  # 用户所在部门
    password = models.CharField(max_length=LONG_INFO_LEN)  # 用户密码(加密后)
    username = models.CharField(max_length=NAME_LEN)  # 用户用于登录的用户名
    avatar = models.ImageField()  # 用户头像
    bio = models.CharField(max_length=LONG_INFO_LEN)  # 签名
    entryTime = models.DateTimeField(null=True)  # 用户入职时间
    employeeType = models.CharField(max_length=SHORT_INFO_LEN)  # 员工类型
    graduationTime = models.DateTimeField(null=True)  # 毕业时间
    registrationTime = models.DateTimeField(auto_now_add=True)  # 注册时间
    superior = models.CharField(max_length=NAME_LEN)  # 直属上级
    detail = models.CharField(max_length=1000)  # 入职情况和详细信息
    historicalMembers = models.IntegerField(default=0)  # 历史带新人数
    currentMembers = models.IntegerField(default=0)  # 当前带新人数
    isAdmin = models.BooleanField(default=False)  # 是否是管理员
    isTeacher = models.BooleanField(default=False)  # 是否是老师
    isHRBP = models.BooleanField(default=False)  # 是否是HRBP
    isNew = models.BooleanField(default=False)  # 是否是新人


class ProgramTable(models.Model):
    """
    大的培训项目的表
    """
    id = models.CharField(primary_key=True, max_length=NAME_LEN)  # 项目id
    name = models.CharField(max_length=NAME_LEN)  # 项目名称
    author = models.ForeignKey(PrivateInfo, on_delete=models.PROTECT)  # 项目作者或者管理者
    intro = models.CharField(max_length=LONG_INFO_LEN)  # 项目简介
    tag = models.CharField(max_length=LONG_INFO_LEN)  # 项目标签
    subItemNum = models.IntegerField()  # 子项目数
    beginTime = models.DateTimeField()  # 项目开始时间
    finishTime = models.DateTimeField()  # 项目结束时间
    deadline = models.DateTimeField()  # 项目对于个人来书都ddl
    audience = models.IntegerField()  # 项目受众
    cover = models.ImageField()  # 项目封面
    releaseTime = models.DateTimeField(auto_now_add=True)  # 发布时间


class EventTable(models.Model):
    """
    包括course exam task
    """
    id = models.CharField(primary_key=True, max_length=NAME_LEN)  # 事件id
    name = models.CharField(max_length=NAME_LEN)  # 事件名称
    author = models.ForeignKey(PrivateInfo, on_delete=models.PROTECT, blank=True)  # 事件作者
    intro = models.CharField(max_length=LONG_INFO_LEN)  # 事件简介
    tag = models.CharField(max_length=LONG_INFO_LEN)  # 事件标签
    subItemNum = models.IntegerField()  # 子项目数
    recommendedTime = models.IntegerField()  # 建议用时
    audience = models.IntegerField()  # 受众
    cover = models.ImageField()  # 封面
    type = models.IntegerField()  # 事件类型
    isTemplate = models.BooleanField()  # 是否是模板
    taskType = models.IntegerField()  # 任务类型(针对task类)
    text = models.CharField(max_length=10000)  # 任务文字(针对task类)
    link = models.CharField(max_length=LONG_INFO_LEN)  # 任务链接
    programId = models.ForeignKey(ProgramTable, on_delete=models.CASCADE)  # 所属的Programid
    releaseTime = models.DateTimeField(auto_now_add=True)  # 发布时间


class LessonTable(models.Model):
    """
    课程库,隶属于培训内容库
    """
    id = models.CharField(primary_key=True, max_length=NAME_LEN)  # 课堂id
    name = models.CharField(max_length=NAME_LEN)  # 课堂名称
    author = models.ForeignKey(PrivateInfo, on_delete=models.PROTECT, blank=True)  # 课堂作者
    event = models.ForeignKey(EventTable, on_delete=models.CASCADE)  # 课堂所属的事件或者大课程
    intro = models.CharField(max_length=LONG_INFO_LEN)  # 课堂介绍
    recommendedTime = models.IntegerField()  # 建议用时
    cover = models.ImageField()  # 封面
    releaseTime = models.DateTimeField(auto_now_add=True)  # 发布时间


class CoursewareTable(models.Model):
    """
    课件库
    """
    id = models.CharField(primary_key=True, max_length=NAME_LEN)  # 课件id
    lesson = models.ForeignKey(LessonTable, on_delete=models.PROTECT)  # 所属课堂
    event = models.ForeignKey(EventTable, on_delete=models.PROTECT)  # 所属课程或事件
    name = models.CharField(max_length=NAME_LEN)  # 名称
    cover = models.ImageField()  # 封面
    uploadTime = models.DateTimeField(auto_now_add=True)  # 上传时间
    url = models.CharField(max_length=LONG_INFO_LEN)  # 课件地址
