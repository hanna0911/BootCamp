"""
app设置文件
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    用于app的设置
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
