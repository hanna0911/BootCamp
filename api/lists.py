import json
import logging

from django.http import HttpRequest
from .api_util import gen_response, role_authentication, load_private_info
from .models import PrivateInfo,UserProgramTable


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
    logging.error(return_list)
    return gen_response(200, return_list)


def nominate_process(req: HttpRequest):
    username = req.session.get("username", None)
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
        # program_relations = teacher.ProgramsAsUser.get()


    return gen_response(400, message="not supported")


def duty_teacher_list(req: HttpRequest):
    return gen_response(400, message="not supported      ")
