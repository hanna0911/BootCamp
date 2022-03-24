from django.urls import path
from . import views


# api应用的路由配置
urlpatterns = [
    path('login', views.login, name='login'),  # just for test
    path('join', views.join, name='join'),  # just for join
    path("init",views.init_test)
]
