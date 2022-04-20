"""
切换状态，切换关系相关的接口
"""
from django.http import HttpRequest
from .api_util import *
import json


def reject_nominate(req: HttpRequest):
    if not check_method(req, "POST"):
        return gen_response(400, message="invalid method")
    username = req.session.get("username", None)
    if username is None:
        return gen_response(
            400, message="no username in session, probly not login")
    if not role_list_check(username, ['admin', 'HRBP']):
        return gen_response(400, message="no permission")

    try:
        data: dict = json.loads(req.body)
    except Exception:
        return gen_response(400, message='Load json request failed')
    username = data.get("username", None)
    if username is None:
        return gen_response(400, message="no username in body")
    users = PrivateInfo.objects.filter(username=username)
    if len(users) < 1:
        return gen_response(400, "user not found")
    user = users.first()
    user.teacherExaminedStatus = PrivateInfo.EnumTeacherExaminedStatus.Fail
    user.save()
    return gen_response(200)


def accept_nominate(req: HttpRequest):
    if not check_method(req, "POST"):
        return gen_response(400, message="invalid method")
    username = req.session.get("username", None)
    if username is None:
        return gen_response(
            400, message="no username in session, probly not login")
    if not role_list_check(username, ['admin', 'HRBP']):
        return gen_response(400, message="no permission")
    try:
        data: dict = json.loads(req.body)
    except Exception:
        return gen_response(400, message='Load json request failed')
    username = data.get("username", None)
    if username is None:
        return gen_response(400, message="no username in body")
    users = PrivateInfo.objects.filter(username=username)
    if len(users) < 1:
        return gen_response(400, "user not found")
    user = users.first()
    user.teacherExaminedStatus = PrivateInfo.EnumTeacherExaminedStatus.Pass
    user.save()
    return gen_response(200)
