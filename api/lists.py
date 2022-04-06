import json
import logging

from django.http import HttpRequest
from .api_util import gen_response, role_authentication, load_private_info, check_method, role_list_check
from .models import PrivateInfo, UserProgramTable


def admin_newcomer_list(request: HttpRequest):
    """
    接收前端向/admin_newcomer_list的get请求
    获取所有新人的数据
    仅限管理员使用
    TODO
    """

    return gen_response(400, message="not supported")


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
    return gen_response(200, return_list)


def nominate_process(req: HttpRequest):
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
        if status == 0:
            tmp["teacherExaminedStatus"] = "未审核"
        elif status == 1:
            tmp["teacherExaminedStatus"] = "通过"
        elif status == 2:
            tmp["teacherExaminedStatus"] = "拒绝"
        else:
            raise Exception("数据可数据错误，请检查写入接口是否正确")
        user_program = teacher.ProgramsAsUser.filter(program__audience=1).first()
        if user_program.finished:
            tmp["learningStatus"] = "已完成"
        else:
            tmp["learningStatus"] = "进行中"
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
        return_list.append(tmp)
    return gen_response(200, data=return_list, message="send {} data".format(len(return_list)))


def nominated_list(req: HttpRequest):
    return gen_response(400, "not supported")
