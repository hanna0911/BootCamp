from django.urls import path
from . import views, lists

# api应用的路由配置
urlpatterns = [
    path('login', views.login, name='login'),  # just for test
    path('join', views.join, name='join'),  # just for join
    path('switch_role', views.switch_role, name='switch_role'),  # 切换身份
    path("admin_newcomer_list", lists.admin_newcomer_list, name="admin_newcomer_list"),
    path("teacher_wait_list", lists.teacher_wait_list, name="teacher_wait_list"),
    path("nominate_process", lists.nominate_process, name="nominate_process"),
    path("duty_teacher_list", lists.duty_teacher_list, name="duty_teacher_list"),
]
