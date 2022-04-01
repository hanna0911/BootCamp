import json
from django.http import HttpRequest
from .api_util import gen_response, role_authentication


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

    return gen_response(400, message="not supported")


def nominate_process(req: HttpRequest):
    return gen_response(400, message="not supported")


def duty_teacher_list(req: HttpRequest):
    return gen_response(400, message="not supported      ")
