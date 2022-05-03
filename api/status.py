"""
切换状态，切换关系相关的接口
"""
import logging

from django.http import HttpRequest
from django.utils import timezone
from .api_util import *
from .models import TeacherNewcomerTable, ContentTable, PrivateInfo, UserContentTable
import json
import datetime


def reject_nominate(req: HttpRequest):
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["admin", "HRBP"],
        "data_field": ["username"]
    })
    if not ok:
        return res
    data: dict = json.loads(req.body)
    username = data.get("username", None)
    users = PrivateInfo.objects.filter(username=username)
    if len(users) < 1:
        return gen_response(400, "user not found")
    user = users.first()
    user.teacherExaminedStatus = PrivateInfo.EnumTeacherExaminedStatus.Fail
    user.save()
    return gen_response(200)


def accept_nominate(req: HttpRequest):
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["admin", "HRBP"],
        "data_field": ["username"]
    })
    if not ok:
        return res
    data: dict = json.loads(req.body)
    username = data.get("username", None)
    users = PrivateInfo.objects.filter(username=username)
    if len(users) < 1:
        return gen_response(400, "user not found")
    user = users.first()
    user.teacherExaminedStatus = PrivateInfo.EnumTeacherExaminedStatus.Pass
    user.save()
    return gen_response(200)


def nominate_teachers(req: HttpRequest):
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["admin"],
        "data_field": []
    })
    if not ok:
        return res
    data: dict = json.loads(req.body)
    for item in data:
        print(item["username"])
        user = PrivateInfo.objects.get(username=item["username"])
        user.isTeacher = True
        user.teacherNominationDate = timezone.now()
        user.save()
    return gen_response(200, message="success")


def assign_teacher(req: HttpRequest):
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["admin"],
        "data_field": ["teacher", "newcomer"]
    })
    if not ok:
        return res
    data: dict = json.loads(req.body)
    try:
        teacher = PrivateInfo.objects.get(username=data.get("teacher"))
        newcomer = PrivateInfo.objects.get(username=data.get("newcomer"))
    except Exception as e:
        return gen_response(400, "user not found")
    if not (teacher.isTeacher and teacher.teacherIsDuty):
        return gen_response(400, message="teacher field has no teacher permission or teacher not duty")
    if len(TeacherNewcomerTable.objects.filter(newcomer=newcomer)) > 0:
        return gen_response(400, message="muti teacher assigned")
    entry = TeacherNewcomerTable(teacher=teacher, newcomer=newcomer)
    entry.save()
    teacher.currentMembers = teacher.currentMembers + 1
    teacher.save()
    return gen_response(200)


def newcomer_commit_teacher(req: HttpRequest):
    """
    新人给导师评价
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["newcomer"],
        "data_field": ["content"]
    })
    if not ok:
        return res

    return gen_response(400, message="not sup")


def teacher_commit_newcomer(req: HttpRequest):
    """
    导师给新人评价
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["teacher"],
        "data_field": ["content"]
    })
    if not ok:
        return res

    return gen_response(400, message="not sup")


def newcomer_score_teacher(req: HttpRequest):
    """
    新人给导师评分
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["newcomer"],
        "data_field": ["score"]
    })
    if not ok:
        return res
    return gen_response(400, message="not sup")


def teacher_score_newcomer(req: HttpRequest):
    """
    导师给新人评价
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["teacher"],
        "data_field": ["score"]
    })
    if not ok:
        return res

    return gen_response(400, message="not sup")


def assign_content(request: HttpRequest):
    """
    POST{
        "action": "assign content",
        "assigneeID": 被分配内容的用户id
        "contentID": 被分配内容的id
        "deadline": "yyyy-MM-dd HH:mm"
        "obligatory": true/false
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    action = data.get('action')
    assignee_id = data.get('assigneeID')
    content_id = data.get('contentID')
    deadline = data.get('deadline')
    obligatory = data.get('obligatory')
    session = request.session
    username = session.get('username')
    role = session.get('role')
    # print(action, assignee_id, content_id, deadline, obligatory)
    if action != 'assign content' or assignee_id is None or content_id is None \
            or deadline is None or obligatory is None:
        return gen_standard_response(400, {"message": "Bad Arguments"})
    assignee_filter = PrivateInfo.objects.filter(username=assignee_id)
    content_filter = ContentTable.objects.filter(id=content_id)
    assigner_filter = PrivateInfo.objects.filter(username=username)
    if len(assignee_filter) == 0 or len(content_filter) == 0 or len(assigner_filter) == 0:
        return item_not_found_error_response()
    if username is None or role is None:
        return session_timeout_response()
    if role != 'admin' and role != 'teacher' and role != 'HRBP':
        return unauthorized_action_response()
    assignee = assignee_filter.first()
    content = content_filter.first()
    assigner = assigner_filter.first()
    print(deadline)
    try:
        deadline_datetime = datetime.datetime.fromisoformat(deadline)
    except Exception as e:
        print(e)
        return gen_standard_response(400, {"message": "Bad Arguments"})
    entry = UserContentTable(user=assignee, content=content, deadline=deadline_datetime,
                             isObligatory=obligatory, assigner=assigner)
    entry.save()
    if content.type == 0:
        str_type = "course"
    elif content.type == 1:
        str_type = "exam"
    else:
        str_type = "task"
    res = f"content {content.name} of type {str_type} assigned to {assignee.username} with real name {assignee.name}"
    return gen_standard_response(200, {"result": "success",
                                       "message": res})
