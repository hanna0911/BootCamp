"""
切换状态，切换关系相关的接口
"""
import logging

from django.http import HttpRequest
from django.utils import timezone
from .api_util import *
from .models import TeacherNewcomerTable, ContentTable, PrivateInfo, UserContentTable,\
    NewcomerRecode, ProgramTable, UserProgramTable, ProgramContentTable
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
    data = json.loads(req.body)
    # 因为每个新人只有一个导师，所以无需指明导师，也无需说明自己是谁
    newcomer = PrivateInfo.objects.get(username=req.session.get("username"))
    relations = TeacherNewcomerTable.objects.filter(newcomer=newcomer)
    if len(relations) <= 0:
        return gen_response(400, message="newcomer has no teacher")
    relation = relations.first()
    relation.newcomerToTeacher = data.get("content")
    relation.save()
    return gen_response(200)


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
        "data_field": ["content", "newcomer"]
    })
    if not ok:
        return res
    data = json.loads(req.body)
    ok, relation = get_relation(teacher=req.session.get("username"), newcomer=data["newcomer"])
    if not ok:
        return relation
    relation.teacherToNewcomer = data["content"]
    relation.save()
    return gen_response(200)


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
    data = json.loads(req.body)
    # 因为每个新人只有一个导师，所以无需指明导师，也无需说明自己是谁
    newcomer = PrivateInfo.objects.get(username=req.session.get("username"))
    relations = TeacherNewcomerTable.objects.filter(newcomer=newcomer)
    if len(relations) <= 0:
        return gen_response(400, message="newcomer has no teacher")
    relation = relations.first()
    try:
        score = float(data.get("score"))
    except:
        return gen_response(400, message="score not a number")
    relation.teacherScore = score
    relation.save()
    return gen_response(200)


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
        "data_field": ["score", "newcomer"]
    })
    if not ok:
        return res
    data = json.loads(req.body)
    ok, relation = get_relation(teacher=req.session.get("username"), newcomer=data["newcomer"])
    if not ok:
        return relation
    try:
        score = float(data.get("score"))
    except:
        return gen_response(400, message="score not a number")
    relation.newcomerScore = score
    relation.save()
    return gen_response(200)


def newcomer_recode(req: HttpRequest):
    """
    导师写带新记录
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["teacher"],
        "data_field": ["content", "newcomer"]
    })
    if not ok:
        return res
    data = json.loads(req.body)
    teacher = PrivateInfo.objects.get(username=req.session.get("username"))
    ok, newcomer = find_people(data["newcomer"])
    if not ok:
        return newcomer
    relation = TeacherNewcomerTable.objects.filter(teacher=teacher, newcomer=newcomer)
    if len(relation) <= 0:
        return gen_response(400, message="newcomer not belong to teacher")
    recode = NewcomerRecode(
        teacher=teacher,
        newcomer=newcomer,
        content=data["content"],
        commitTime=timezone.now()
    )
    recode.save()
    return gen_response(200)


def get_newcomer_recode(req: HttpRequest):
    """
    获取某个导师和学生的带新记录
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["teacher", "admin"],
        "data_field": ["newcomer"]
    })
    if not ok:
        return res
    data = json.loads(req.body)
    # if req.session.get("role") == "teacher":  # 如果是导师发出的请求，则默认导师是自己
    #     teacher = PrivateInfo.objects.get(username=req.session.get("username"))
    # else:  # 如果是管理员发出的请求，则按照字段中的导师进行寻找
    #     found, teacher = find_people(data["teacher"])
    #     if not found:
    #         return teacher
    found, newcomer = find_people(data["newcomer"])
    if not found:
        return newcomer
    recodes = NewcomerRecode.objects.filter(newcomer=newcomer)
    return_list = []
    for recode in recodes:
        return_list.append({
            "content": recode.content,
            "commitTime": recode.commitTime
        })
    return gen_response(200, return_list)


def get_commits_and_score(req: HttpRequest):
    """
    获取导师和学生之间的相互评价和打分
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["admin"],
        "data_field": ["newcomer"]  # 只需要确认新人，就可以找到评论，无需导师信息
    })
    if not ok:
        return res
    data = json.loads(req.body)
    found, newcomer = find_people(data["newcomer"])
    if not found:
        return newcomer
    relations = TeacherNewcomerTable.objects.filter(newcomer=newcomer)
    if len(relations) <= 0:
        return gen_response(400, message="newcomer has no teacher")
    relation = relations.first()
    ret_data = {
        "teacherScore": relation.teacherScore,
        "newcomerScore": relation.newcomerScore,
        "newcomerToTeacher": relation.newcomerToTeacher,
        "teacherToNewcomer": relation.teacherToNewcomer
    }
    return gen_response(200, ret_data)

# def assign_program(request: HttpRequest):
#     """
#     POST{
#         'action': 'assign program',
#         'assigneeID': 被分配program的用户id,
#         'programID': 被分配program的id,
#         'deadline': "yyyy-MM-dd HH:mm"
#     }
#     """
#     if request.method != 'POST':
#         return illegal_request_type_error_response()
#     try:
#         data = json.loads(request.body)
#     except Exception as e:
#         print(e)
#         return unknown_error_response()
#     action = data.get('action')
#     assignee_id = data.get('assigneeID')
#     program_id = data.get('programID')
#     deadline_str = data.get('deadline')
#     session = request.session
#     username = session.get('username')
#     role = session.get('role')
#     if action != 'assign program' or assignee_id is None or program_id is None or deadline_str is None:
#         return gen_standard_response(400, {"message": "Bad Arguments"})
#     assignee_filter = PrivateInfo.objects.filter(username=assignee_id)
#     program_filter = ProgramTable.objects.filter(id=program_id)
#     assigner_filter = PrivateInfo.objects.filter(username=username)
#     if len(assignee_filter) == 0 or len(program_filter) == 0 or len(assigner_filter) == 0:
#         return item_not_found_error_response()
#     if username is None or role is None:
#         return session_timeout_response()
#     if role != 'admin' and role != 'teacher' and role != 'HRBP':
#         return unauthorized_action_response()
#     assignee = assignee_filter.first()
#     program = program_filter.first()
#     assigner = assigner_filter.first()
#     print(deadline_str)
#     try:
#         deadline_datetime = datetime.datetime.fromisoformat(deadline_str)
#     except Exception as e:
#         print(e)
#         return gen_standard_response(400, {"message": "Bad Arguments"})
#     entry = UserProgramTable(user=assignee, program=program,\
#                              deadline=deadline_datetime, assigner=assigner)
#     entry.save()
#     if program.isTemplate:
#         ack = 'a'
#     else:
#         ack = 'not a'
#     res = f"program {program.name} which is {ack} template assigned to {assignee.username} with real name {assignee.name}"
#     return gen_standard_response(200, {"result": "success",
#                                        "message": res})


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


def has_program(request: HttpRequest):
    """
    POST
    {
        'action': 'has program'
        'username': __USERNAME__
    }
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    action = data.get('action')
    target_username = data.get('username')
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if action != 'has program' or target_username is None:
        return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
    if username is None or role is None:
        return session_timeout_response()
    target_user = PrivateInfo.objects.filter(username=target_username).first()
    if role != 'teacher' and role != 'admin' and role != 'HRBP':
        return unauthorized_action_response()
    if target_user is None:
        return item_not_found_error_response()
    relation = UserProgramTable.objects.filter(user__username=target_username).first()
    if relation is None:
        return gen_standard_response(200, {'result': 'success',
                                           'message': f'user {target_username} has not been assigned a program',
                                           'hasProgram': False,
                                           'programID': ''})
    else:
        return gen_standard_response(200, {'result': 'success',
                                           'message': f'user {target_username} has been assigned a program',
                                           'hasProgram': True,
                                           'programID': relation.program.id})


def assign_program(request: HttpRequest):
    """
    POST
    {
        'action': 'assign program',
        'username': __USERNAME__,
        'programID': __PROGRAM_ID__
    }
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    action = data.get('action')
    target_username = data.get('username')
    target_program_id = data.get('programID')
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if action != 'assign program' or target_username is None or target_program_id is None:
        return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
    if username is None or role is None:
        return session_timeout_response()
    if role != 'admin' and role != 'HRBP' and role != 'teacher':
        return unauthorized_action_response()
    target_user = PrivateInfo.objects.filter(username=target_username).first()
    target_program = ProgramTable.objects.filter(id=target_program_id).first()
    assigner = PrivateInfo.objects.filter(username=username).first()
    if target_program is None or target_user is None:
        return item_not_found_error_response()
    new_user_program_relation = UserProgramTable(user=target_user, program=target_program, assigner=assigner)
    new_user_program_relation.save()
    content_relations = ProgramContentTable.objects.filter(program__id=target_program_id)
    for content_relation in content_relations:
        content = content_relation.content
        new_user_content_relation = UserContentTable(user=target_user, content=content, assigner=assigner, deadline = 0)
        new_user_content_relation.save()
    std_message = f'added program {target_program_id} to user {target_username}\'s list of programs, including '\
                  + f'{len(content_relations)} contents'
    return gen_standard_response(200, {'result': 'success',
                                       'message': std_message})
