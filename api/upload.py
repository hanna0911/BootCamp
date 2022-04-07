"""
所有上传新内容相关的接口
"""
import time

from django.http import HttpRequest
from .api_util import *
from .models import *
import json


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
    action = data.get("action")
    name = data.get("name")
    intro = data.get("intro")
    tag = data.get("tag")
    recommend_time = data.get("recommendTime")
    audience = data.get("audience")
    cover = data.get("cover")
    if action != "create program" or name is None or name == "" \
            or audience is None or (audience != "newcomer" and audience != "teacher"):
        return gen_standard_response(400, {"result": "failure", "message": "bad arguments"})
    if intro is None or intro == "":
        intro = "暂无简介"
    if audience == "teacher":
        audience_id = 1
    else:
        audience_id = 0
    new_program_id = user_session["user"] + "_p_" + str(time.time())
    new_program = ProgramTable(id=new_program_id, name=name, author=user_session["user"],
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
    action = data.get("action")
    name = data.get("name")
    intro = data.get("intro")
    tag = data.get("tag")
    recommend_time = data.get("time")
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
    if action is None or (action != "create content template" and action != "create content") \
            or name is None or name == "" \
            or content_type is None or (content_type != "course" and content_type != "exam" and content_type != "task") \
            or audience is None or (audience != "teacher" and audience != "newcomer") \
            or is_template is None or (is_template != "true" and is_template != "false") \
            or program_id is None or len(ProgramTable.objects.filter(id=program_id)) == 0:
        return gen_standard_response(400, {"result": "failure", "message": "bad arguments"})
    if content_type == "exam" and csv is None:
        return gen_standard_response(400, {"result": "failure", "message": "exam paper not found"})
    if content_type == "task" and ((task_type == 0 and (task_text is None or task_text == ""))
                                   or (task_type == 1 and (task_link is None or task_link == ""))
                                   or (task_type == 2 and task_file is None)):
        return gen_standard_response(400, {"result": "failure", "message": "task content not found"})
    user_session = request.session
    if user_session is None or "role" not in user_session.keys() or "user" not in user_session.keys():  # session不存在
        return session_timeout_response()
    username = user_session["name"]
    cur_role = user_session["role"]
    if is_template == "true" and cur_role != "admin":
        return unauthorized_action_response()
    if is_template == "false" and cur_role != "admin" and cur_role != "teacher":
        return unauthorized_action_response()
    if intro is None or intro == "":
        intro = "暂无简介"
    new_content_id = username + "_c_" + str(time.time())
    if audience == "teacher":
        audience_id = 1
    else:
        audience_id = 0
    if is_template == "true":
        is_template_bool = True
    else:
        is_template_bool = False
    if content_type == "course":
        content_type_id = 0
    elif content_type == "exam":
        content_type_id = 1
    else:
        content_type_id = 2
    new_content = ContentTable(id=new_content_id, name=name, author=username,
                               intro=intro, tag=tag, recommendedTime=recommend_time,
                               audience=audience_id, cover=cover, type=content_type_id,
                               isTemplate=is_template_bool, programId=program_id,
                               lessonCount=0, questions=csv, taskType=task_type,
                               text=task_text, link=task_link, taskFile=task_file)
    new_content.save()
    program = ProgramTable.objects.filter(id=program_id).first()
    new_program_content_relation = ProgramContentTable(program=program, content=new_content)
    new_program_content_relation.save()
    program.contentCount += 1
    return gen_standard_response(200, {
        "result": "success",
        "message": f"content {name} created successfully",
        "contentID": new_content_id
    })
