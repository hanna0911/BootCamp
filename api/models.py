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
    username = models.CharField(max_length=SHORT_INFO_LEN)  # 用户用于登录的用户名
    avatar = models.ImageField()  # 用户头像
    bio = models.CharField(max_length=LONG_INFO_LEN)  # 签名
    entryTime = models.DateTimeField()  # 用户入职时间
    employeeType = models.CharField(max_length=SHORT_INFO_LEN)  # 员工类型
    graduationTime = models.DateTimeField()  # 毕业时间
    registrationTime = models.DateTimeField(auto_now_add=True)  # 注册时间
    superior = models.CharField(max_length=NAME_LEN)  # 直属上级
    detail = models.CharField(1000)  # 入职情况和详细信息
    historicalMembers = models.IntegerField(default=0)  # 历史带新人数
    currentMembers = models.IntegerField(default=0)  # 当前带新人数
    isAdmin = models.BooleanField()  # 是否是管理员
    isTeacher = models.BooleanField()  # 是否是老师
    isHRBP = models.BooleanField()  # 是否是HRBP
    isNew = models.BooleanField()  # 是否是新人


class ProgramTable(models.Model):
    """
    大的培训项目的表
    """
    id = models.CharField(primary_key=True, max_length=NAME_LEN)
    name = models.CharField(max_length=NAME_LEN)
    author = models.ForeignKey(PrivateInfo, on_delete=models.PROTECT)
    intro = models.CharField(max_length=LONG_INFO_LEN)
    tag = models.CharField(max_length=LONG_INFO_LEN)
    subItemNum = models.IntegerField()
    beginTime = models.DateTimeField()
    finishTime = models.DateTimeField()
    deadline = models.DateTimeField()
    audience = models.IntegerField()
    cover = models.ImageField()


class EventTable(models.Model):
    """
    包括course exam task
    """
    id = models.CharField(primary_key=True, max_length=NAME_LEN)
    name = models.CharField(max_length=NAME_LEN)
    author = models.ForeignKey(PrivateInfo, on_delete=models.PROTECT, blank=True)
    intro = models.CharField(max_length=LONG_INFO_LEN)
    tag = models.CharField(max_length=LONG_INFO_LEN)
    subItemNum = models.IntegerField()
    recommendedTime = models.IntegerField()
    audience = models.IntegerField()
    cover = models.ImageField()
    class_ = models.IntegerField()
    isTemplate = models.BooleanField()
    taskType = models.IntegerField()
    text = models.CharField(max_length=10000)
    link = models.CharField(LONG_INFO_LEN)
    programId = models.ForeignKey(ProgramTable, on_delete=models.CASCADE)


class LessonTable(models.Model):
    """
    课程库,隶属于培训内容库
    """
    id = models.CharField(primary_key=True, max_length=NAME_LEN)
    name = models.CharField(max_length=NAME_LEN)
    author = models.ForeignKey(PrivateInfo, on_delete=models.PROTECT, blank=True)
    course = models.ForeignKey(EventTable, on_delete=models.CASCADE)
    intro = models.CharField(max_length=LONG_INFO_LEN)
    recommendedTime = models.IntegerField()
    cover = models.ImageField()
    releaseTime = models.DateTimeField()


class CoursewareTable(models.Model):
    """
    课件库
    """
    id = models.CharField(primary_key=True, max_length=NAME_LEN)
    lesson = models.ForeignKey(LessonTable, on_delete=models.SET_NULL)
    event = models.ForeignKey(EventTable, on_delete=models.SET_NULL)
    name = models.CharField(max_length=NAME_LEN)
    cover = models.ImageField()
    uploadTime = models.DateTimeField()
    url = models.CharField(max_length=LONG_INFO_LEN)
