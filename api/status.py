"""
切换状态，切换关系相关的接口
"""
import logging

from django.http import HttpRequest
from django.utils import timezone
from .api_util import *
from .models import TeacherNewcomerTable
import json


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
        user.isTeacher =True
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
    entry = TeacherNewcomerTable(teacher=teacher, newcomer=newcomer)
    entry.save()
    teacher.currentMembers = teacher.currentMembers + 1
    teacher.save()
    return gen_response(200)
