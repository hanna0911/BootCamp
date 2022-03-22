from django.db import models

'''
描述数据库结构的文件
'''


# Create your models here.

class User(models.Model):
    """
    user table
    """
    name = models.CharField(max_length=50)
