"""
所有上传新内容相关的接口
此文件全部接口作者：@yzt
"""
import os.path
import time

import django.core.files.uploadedfile
from django.http import HttpRequest
from .api_util import *
from .models import *
import json

MAX_ALLOWED_COURSEWARES_FOR_ONE_LESSON = 10

def create_program(request: HttpRequest):
    """
    创建一个Program
    """
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception:
        return gen_response(400, 'Load json request failed')
    user_session = request.session
    if user_session is None or "role" not in user_session.keys():  # session不存在
        return session_timeout_response()
    if user_session["role"] != "admin" and user_session["role"] != "teacher":  # 权限认证
        return unauthorized_action_response()
    # 从json中读取请求信息
    action = data.get("action")
    name = data.get("name")
    intro = data.get("intro")
    tag = data.get("tag")
    recommend_time = data.get("recommendTime")
    audience = data.get("audience")
    cover = data.get("cover")
    # 校验action字段、name字段和audience字段是否合规
    if action != "CreateProgram" or name is None or name == "" \
            or audience is None or (audience != "newcomer" and audience != "teacher"):
        return gen_standard_response(400, {"result": "failure", "message": "bad arguments"})
    if intro is None or intro == "":  # 无简介的话生成默认简介
        intro = "暂无简介"
    if audience == "teacher":  # API字段转换为数据库阶段
        audience_id = 1
    else:
        audience_id = 0
    username = user_session['username']
    new_program_id = username + "_p_" + str(time.time())  # 生成ProgramID 规则: username_p_time
    user = PrivateInfo.objects.filter(username=username).first() # 外键
    new_program = ProgramTable(id=new_program_id, name=name, author=user,
                               intro=intro, tag=tag, contentCount=0, recommendTime=recommend_time,
                               audience=audience_id, cover=cover)
    new_program.save()
    return gen_standard_response(200, {"result": "success",
                                       "message": f"program {name} created successfully",
                                       "programID": new_program_id})


def create_content(request: HttpRequest):
    """
    创建一个content(课程/考试/任务)
    """
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception:
        return gen_response(400, 'Load json request failed')
    # 读取信息
    action = data.get("action")
    name = data.get("name")
    intro = data.get("intro")
    tag = data.get("tag")
    recommend_time = data.get("recommendTime")
    audience = data.get("audience")
    cover = data.get("cover")
    content_type = data.get("type")
    is_template = data.get("isTemplate")
    csv = data.get("csv")
    program_id = data.get("programID")
    task_type = data.get("taskType")
    task_text = data.get("taskText")
    task_link = data.get("taskLink")
    task_file = data.get("taskFile")
    # 这个巨大的if用于校验请求信息是否合规
    # 第1行 - action字段校验
    # 第2行 - name字段校验
    # 第3行 - audience字段校验
    # 第4行 - isTemplate字段校验
    # 第5行 - programID有效性校验
    if action is None or (action != "CreateContentTemplate" and action != "create content")\
            or name is None or name == ""\
            or content_type is None or (content_type != "course" and content_type != "exam" and content_type != "task")\
            or audience is None or (audience != "teacher" and audience != "newcomer")\
            or is_template is None or (is_template is not True and is_template is not False)\
            or program_id is None or len(ProgramTable.objects.filter(id=program_id)) == 0:
        return gen_standard_response(400, {"result": "failure", "message": "bad arguments"})
    if content_type == "exam" and csv is None:  # exam类型的content必须有考题csv文件
        return gen_standard_response(400, {"result": "failure", "message": "exam paper not found"})
    if content_type == "task" and ((task_type == 0 and (task_text is None or task_text == ""))  # 文字型task必需有文字
                                   or (task_type == 1 and (task_link is None or task_link == ""))  # 链接型task必须有链接
                                   or (task_type == 2 and task_file is None)):  # 文件型task必须有文件
        return gen_standard_response(400, {"result": "failure", "message": "task content not found"})
    user_session = request.session
    if user_session is None or "role" not in user_session.keys() or "username" not in user_session.keys():  # session不存在
        return session_timeout_response()
    username = user_session['username']
    cur_role = user_session["role"]
    user = PrivateInfo.objects.filter(username=username).first()
    program = ProgramTable.objects.filter(id=program_id).first()
    if is_template == True and cur_role != "admin":
        return unauthorized_action_response()
    if is_template == False and cur_role != "admin" and cur_role != "teacher":
        return unauthorized_action_response()
    if intro is None or intro == "":
        intro = "暂无简介"
    new_content_id = username + "_c_" + str(time.time())  # 与program类似的ID生成机制
    if audience == "teacher":
        audience_id = 1
    else:
        audience_id = 0
    if is_template == "true":  # isTemplate字段转换
        is_template_bool = True
    else:
        is_template_bool = False
    if content_type == "course":  # type字段转换
        content_type_id = 0
    elif content_type == "exam":
        content_type_id = 1
    else:
        content_type_id = 2
    new_content = ContentTable(id=new_content_id, name=name, author=user,
                               intro=intro, tag=tag, recommendedTime=recommend_time,
                               audience=audience_id, cover=cover, type=content_type_id,
                               isTemplate=is_template, programId=program,
                               lessonCount=0, questions=csv, taskType=task_type,
                               text=task_text, link=task_link, taskFile=task_file)
    new_content.save()
    new_program_content_relation = ProgramContentTable(program=program, content=new_content)  # 和父program创建关联信息
    new_program_content_relation.save()
    program.contentCount += 1  # 父program的content数量累加
    return gen_standard_response(200, {
        "result": "success",
        "message": f"content {name} created successfully",
        "contentID": new_content_id
    })


def create_lesson(request: HttpRequest):
    """
    创建一个Lesson
    代码结构和create_content完全一致，就不重复注释了
    """
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception:
        return gen_response(400, 'Load json request failed')
    action = data.get("action")
    name = data.get("name")
    intro = data.get("intro")
    recommend_time = data.get("recommendTime")
    cover = data.get("cover")
    is_template = data.get("isTemplate")
    content_id = data.get("contentID")
    if action is None or (action != "CreateLessonTemplate" and action != "create lesson")\
            or name is None or name == ""\
            or is_template is None or (is_template is not True and is_template is not False)\
            or content_id is None or len(ContentTable.objects.filter(id=content_id)) == 0:
        return gen_standard_response(400, {"result": "failure", "message": "bad arguments"})
    user_session = request.session
    if user_session is None or "role" not in user_session.keys() or "username" not in user_session.keys():  # session不存在
        return session_timeout_response()
    username = user_session['username']
    cur_role = user_session["role"]
    user = PrivateInfo.objects.filter(username=username).first()
    content = ContentTable.objects.filter(id=content_id).first()
    if is_template == True and cur_role != "admin":
        return unauthorized_action_response()
    if is_template == False and cur_role != "admin" and cur_role != "teacher":
        return unauthorized_action_response()
    if intro is None or intro == "":
        intro = "暂无简介"
    new_lesson_id = username + "_l_" + str(time.time())
    new_lesson = LessonTable(id=new_lesson_id, name=name, author=user, content=content,
                             intro=intro, recommendedTime=recommend_time, cover=cover)
    new_lesson.save()
    content.lessonCount += 1
    return gen_standard_response(200, {
        "result": "success",
        "message": f"lesson {name} created successfully",
        "contentID": new_lesson_id
    })


# def save_courseware_file(lesson_id, order, creator_username, dir_prefix, file):
#     file_ext = file.name.split(".")[-1].lower()
#     file_path = f"{dir_prefix}/{lesson_id}/"
#     file_dir = f"{dir_prefix}/{lesson_id}/{order}_{file.name}"
#     try:
#         if not os.path.exists(file_path):
#             os.makedirs(file_path)
#         with open(file_dir, "wb+") as dest:
#             for chunk in file.chunks():
#                 dest.write(chunk)
#     except Exception:
#         return False, file_dir
#     return True, file_dir
#
#
# def upload_courseware(request: HttpRequest):
#     if request.method != "POST":  # 只接受POST请求
#         return illegal_request_type_error_response()
#     try:
#         data = json.loads(request.body)
#     except Exception:
#         return gen_response(400, 'Load json request failed')
#     order = data.get('order')
#     lesson_id = data.get('lessonID')
#     cover = data.get('cover')
#     if order not in range(1, MAX_ALLOWED_COURSEWARES_FOR_ONE_LESSON):
#         return gen_standard_response(400, {"result": "failed", "message": "too many coursewares"})
#     if len(LessonTable.objects.filter(id=lesson_id)) == 0:
#         return gen_standard_response(400, {"result": "failed", "message": "lesson not found"})
#     user_session = request.session
#     if user_session is None or "role" not in user_session.keys() or "user" not in user_session.keys():  # session不存在
#         return session_timeout_response()
#     username = user_session["username"]
#     cur_role = user_session["role"]
#     if cur_role != "admin" or cur_role != "teacher":  # 身份不是管理员或者导师
#         return unauthorized_action_response()
#     file_op_ret = save_courseware_file(lesson_id, order, username, 'files/courseware',
#                                            request.FILES.get("content"))
#     if file_op_ret[0]:
#         new_courseware_id = username + "_cw_" + str(time.time())
#         lesson = LessonTable.objects.filter(id=lesson_id).first()
#         content = lesson.content
#         new_courseware = CoursewareTable(id=new_courseware_id, lesson=lesson_id, content=content,
#                                          name=request.FILES.get("content").name, cover=cover, url=file_op_ret[1])
#         new_courseware.save()
#         std_success_message = f"courseware for lesson {lesson_id} uploaded successfully"
#         return gen_standard_response(200, {"result": "success", "message": std_success_message})
#     else:
#         std_error_message = "file system failed to save uploaded file. better luck next time:("
#         return gen_standard_response(400, {"result": "success", "message": std_error_message})



