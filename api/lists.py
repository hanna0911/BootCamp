import json
import logging

from django.http import HttpRequest
from .api_util import gen_response, role_authentication, load_private_info, check_method, role_list_check, quick_check
from .models import *


def admin_newcomer_list(request: HttpRequest):
    """
    接收前端向/admin_newcomer_list的get请求
    获取所有新人的数据
    仅限管理员使用
    TODO
    """
    if not check_method(request, "GET"):
        return gen_response(400, message="invalid method")
    username = request.session.get("username", None)
    if username is None:
        return gen_response(400, message="no username in session, probly not login")
    if not role_authentication(username, "admin"):
        return gen_response(400, message="permission deny")

    newcomer_list = PrivateInfo.objects.filter(isNew=True, isTeacher=False, isAdmin=False, isHRBP=False)
    return_list = []
    for newcomer in newcomer_list:
        tmp = load_private_info(newcomer)
        teacher_queue = TeacherNewcomerTable.objects.filter(newcomer=newcomer)
        if len(teacher_queue) == 0:
            tmp["tutor"] = "无"
            tmp["teacher"] = "无"
        else:
            tmp["teacher"] = teacher_queue.first().teacher.name
            tmp["tutor"] = teacher_queue.first().teacher.name
        tmp["joinBootcamp"] = True
        tmp["graduated"] = newcomer.newcomerGraduateState  # temp
        tmp["evaluate"] = "暂无"
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(newcomer.username)  # 直接后端指定路径，前端自动请求
        return_list.append(tmp)
    return gen_response(200, return_list, "tmp supported")


def teacher_wait_list(req: HttpRequest):
    """
    权限确认(admin)
    筛选出导师候选人(已经完成新人培训的新人),返回基本信息列表
    :param req:
    :return:
    """
    if not check_method(req, "GET"):
        return gen_response(400, message="invalid method")
    username = req.session.get("username", None)
    if username is None:
        return gen_response(
            400, message="no username in session, probly not login")
    if not role_authentication(username, 'admin'):
        return gen_response(400, message="no permission")
    newcommer_list = PrivateInfo.objects.filter(isTeacher=False, isNew=True)
    return_list = []
    for new in newcommer_list:
        tmp = load_private_info(new)
        return_list.append(tmp)
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(new.username)
    return gen_response(200, return_list)


def nominate_process(req: HttpRequest):
    """
    提名进度列表
    :param req:
    :return:
    """
    username = req.session.get("username", None)
    if not check_method(req, "GET"):
        return gen_response(400, message="invalid method")
    if username is None:
        return gen_response(
            400, message="no username in session, probly not login")
    if not role_authentication(username, 'admin'):
        return gen_response(400, message="no permission")
    teacher_list = PrivateInfo.objects.filter(isTeacher=True, teacherIsDuty=False)
    return_list = []
    for teacher in teacher_list:
        tmp = load_private_info(teacher)
        tmp["teacherNominationDate"] = teacher.teacherNominationDate
        status = teacher.teacherExaminedStatus
        if status == PrivateInfo.EnumTeacherExaminedStatus.NotYet:
            tmp["teacherExaminedStatus"] = "未审核"
        elif status == PrivateInfo.EnumTeacherExaminedStatus.Pass:
            tmp["teacherExaminedStatus"] = "通过"
        elif status == PrivateInfo.EnumTeacherExaminedStatus.Fail:
            tmp["teacherExaminedStatus"] = "拒绝"
        else:
            raise Exception("数据可数据错误，请检查写入接口是否正确")
        user_program = teacher.ProgramsAsUser.filter(program__audience=1).first()
        if user_program is None:
            tmp["learningStatus"] = "未参加"
        elif user_program.finished:
            tmp["learningStatus"] = "已完成"
        else:
            tmp["learningStatus"] = "进行中"
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(teacher.username)
        return_list.append(tmp)
    return gen_response(200, return_list, "send {} data".format(len(return_list)))


def duty_teacher_list(req: HttpRequest):
    if not check_method(req, "GET"):
        return gen_response(400, message="invalid method")
    username = req.session.get("username", None)
    if username is None:
        return gen_response(
            400, message="no username in session, probly not login")
    if not role_list_check(username, ["admin", "HRBP"]):
        return gen_response(400, message="permission denied")
    teacher_list = PrivateInfo.objects.filter(isTeacher=True, teacherIsDuty=True)
    return_list = []
    for teacher in teacher_list:
        tmp = load_private_info(teacher)
        tmp["historicalMembers"] = teacher.historicalMembers
        tmp["currentMembers"] = teacher.currentMembers
        tmp["teacherDutyDate"] = teacher.teacherDutyDate
        tmp["teacherScore"] = teacher.teacherScore
        tmp["OKR"] = "unknown"
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(teacher.username)
        return_list.append(tmp)
    return gen_response(200, data=return_list, message="send {} data".format(len(return_list)))


def nominated_list(req: HttpRequest):
    """
    已经被提名,可以进行审核的教室列表
    :param req:
    :return:
    """
    if not check_method(req, "GET"):
        return gen_response(400, message="invalid method")
    username = req.session.get("username", None)
    if username is None:
        return gen_response(
            400, message="no username in session, probly not login")
    if not role_list_check(username, ["HRBP", "admin"]):  # 暂时做修改适应前端
        return gen_response(400, message="permission denied")
    teacher_list = PrivateInfo.objects.filter(isTeacher=True, teacherIsDuty=False)
    # TODO:获取培训状态
    return_list = []
    for teacher in teacher_list:
        tmp = load_private_info(teacher)
        tmp["teacherNominationDate"] = teacher.teacherNominationDate
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(teacher.username)
        return_list.append(tmp)
    return gen_response(200, data=return_list)


def teacher_newcomer_list(req: HttpRequest):
    """
    获得老师自己带的学生列表(已经毕业的不算)
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "GET",
        "username": "",
        "role": ["teacher"],
    })
    if not ok:
        return res
    teacher = PrivateInfo.objects.get(username=req.session.get("username"))
    student_list = TeacherNewcomerTable.objects.filter(teacher=teacher)
    learning_list = []
    for entry in student_list:  # 还在学习的学生
        if entry.newcomer.newcomerGraduateState == PrivateInfo.EnumNewcomerGraduateState.NotGraduate:
            learning_list.append(entry.newcomer)
    return_list = []
    for newcomer in learning_list:
        tmp = load_private_info(newcomer)
        tmp["graduated"] = GraduateStatusToTest[newcomer.newcomerGraduateState]  # temp
        tmp["evaluate"] = "暂无"
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(newcomer.username)  # 直接后端指定路径，前端自动请求
        return_list.append(tmp)

    return gen_response(200, data=return_list)
