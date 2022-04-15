from django.urls import path
from . import views, lists, upload, download
from backend.write_db import write_db

# api应用的路由配置
urlpatterns = [    path("write_db", write_db),
    path('login', views.login, name='login'),  # just for test
    path('join', views.join, name='join'),  # just for join
    path("get_user_info", views.get_user_info, name="get_user_info"),
    path('switch_role', views.switch_role, name='switch_role'),  # 切换身份
    path('logout', views.logout, name='logout'),  # 登出
    path("admin_newcomer_list", lists.admin_newcomer_list, name="admin_newcomer_list"),
    path("teacher_wait_list", lists.teacher_wait_list, name="teacher_wait_list"),
    path("nominate_process", lists.nominate_process, name="nominate_process"),
    path("duty_teacher_list", lists.duty_teacher_list, name="duty_teacher_list"),
    path("get_token", views.get_token, name="get_token"),
    path("newcomer_info", views.newcomer_info, name="newcomer_info"),
    path("nominated_list", lists.nominated_list, name="nominated_list"),
    path("create_program", upload.create_program, name="create_program"),
    path("admin_create_content_template", upload.create_content, name="create_content_template"),
    path("admin_create_lesson_template", upload.create_lesson, name="create_lesson_template"),
    path("video/", download.stream_video, name="video"),
    path("avatar_by_name/", views.avatar_by_name, name="avatar_by_name"),
    path("avatar", views.avatar, name="avatar")
]
