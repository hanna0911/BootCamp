from django.http import HttpRequest
from .api_util import gen_response


def admin_newcomer_list(request: HttpRequest):
    """
    接收前端向/admin_newcomer_list的get请求
    获取所有新人的数据
    仅限管理员使用
    TODO
    """

    return gen_response(400, message="not supported")


def teacher_wait_list(req: HttpRequest):
    return gen_response(400, message="not supported")


def nominate_process(req: HttpRequest):
    return gen_response(400, message="not supported")


def duty_teacher_list(req: HttpRequest):
    return gen_response(400, message="not supported      ")
