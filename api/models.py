'''
描述数据库结构的文件
'''

from django.db import models


# Create your models here.

class PrivateInfo(models.Model):
    """
    user table
    """
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    dept = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    userid = models.CharField(max_length=50)
    avatar = models.ImageField()
    bio = models.CharField(max_length=200)  # 签名
