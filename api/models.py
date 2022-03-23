'''
描述数据库结构的文件
'''

from django.db import models

# Create your models here.

NAME_LEN = 50
SHORT_INFO_LEN = 20


class PrivateInfo(models.Model):
    """
    user table
    """
    name = models.CharField(max_length=NAME_LEN)  # 用户的真实姓名
    city = models.CharField(max_length=SHORT_INFO_LEN)  # 用户所在城市
    dept = models.CharField(max_length=SHORT_INFO_LEN)  # 用户所在部门
    password = models.CharField(max_length=200)  # 用户密码(加密后)
    username = models.CharField(max_length=SHORT_INFO_LEN)  # 用户用于登录的用户名
    avatar = models.ImageField()  # 用户头像
    bio = models.CharField(max_length=200)  # 签名
    entryTime = models.DateTimeField()  # 用户入职时间
    employeeType = models.CharField(max_length=SHORT_INFO_LEN)  # 员工类型
    graduationTime = models.DateTimeField()  # 毕业时间
    registrationTime = models.DateTimeField(auto_now_add=True)  # 注册时间
    superior = models.CharField(max_length=NAME_LEN)  # 直属上级
    detail = models.CharField(1000)  # 入职情况和详细信息
