from django.urls import path
from . import views, lists, upload, download, status, analysis
from backend.write_db import write_db

# api应用的路由配置
urlpatterns = [
    path("write_db", write_db),
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
    path("avatar", views.avatar, name="avatar"),
    path("upload_courseware_info", upload.upload_courseware_info, name="upload_courseware_info"),
    path("upload_courseware_file", upload.upload_courseware_file, name="upload_courseware_file"),
    path("reject_nominate", status.reject_nominate, name="reject_nominate"),
    path("accept_nominate", status.accept_nominate, name="accept_nominate"),
    path("assign_teacher", status.assign_teacher, name="assign_teacher"),
    path("bootcamp_attend", analysis.bootcamp_attend, name="bootcamp_attend"),
    path("newcomer_average_score", analysis.newcomer_average_score, name="newcomer_average_score"),
    path("teacher_average_score", analysis.teacher_average_score, name="teacher_average_score"),
    path("graduate_time", analysis.graduate_time, name="graduate_time"),
    path("camp_completion", analysis.camp_completion, name="camp_completion"),
    path('upload_test_file', upload.upload_test_file, name="upload_test_file"),
    path('upload_lesson_file', upload.upload_lesson_file, name="upload_lesson_file"),
    path('download_test_info', download.retrieve_test_info_by_id, name="download_test_info"),
    path('download_test_paper', download.retrieve_test_paper_by_id, name="download_test_paper"),
    path('upload_answers', upload.upload_answers, name="upload_answers"),
    path('assignable_test_list', lists.assignable_test_list, name="assignable_test_list"),
    path('my_test_list', lists.my_test_list, name="my_test_list"),
    path('assignable_course_list', lists.assignable_course_list, name="assignable_course_list"),
    path('my_course_list', lists.my_courses_list, name="my_course_list"),
    #path('assign_content', status.assign_content, name="assign content"),
    path("teacher_newcomer_list", lists.teacher_newcomer_list, name="teacher_newcomer_list"),
    path("get_honor", views.get_honor, name="get_honor")
]
