"""
数据分析相关的api接口
"""

import datetime
from json import JSONDecodeError
import logging
from typing import Tuple
from django.http import HttpRequest
from .api_util import *
from .models import *
from django.db.models import QuerySet, Avg


def check_day(date: datetime.datetime, day_start: bool) -> bool:
    if day_start:  # check is day start 00:00:00
        return date.hour == 0 and date.minute == 0 and date.second == 0
    # check is day end 23:59:59
    return date.hour == 23 and date.minute == 59 and date.second == 59


def date_ranges(startDate: datetime.datetime, endDate: datetime.datetime, delta: datetime.timedelta = datetime.timedelta(seconds = 86400)) \
        -> Tuple[(datetime.datetime, datetime.datetime)]:
    days_minus1 = (endDate - startDate).days
    startList = [startDate]
    endList = [endDate]
    for _ in range(days_minus1):
        startList.append(startList[-1] + delta)
        endList.append(endList[-1] - delta)
    endList.reverse()
    return list(zip(startList, endList))


def average_score(users: QuerySet) -> float:
    userprograms = [user.ProgramsAsUser.all() for user in users]
    if len(userprograms) == 0: return 0.0
    if len(userprograms) == 1:
        userprograms = userprograms[0]
    else:
        userprograms = userprograms[0].union(*userprograms[1:])
    return userprograms.aggregate(Avg("score"))["score__avg"]


def bootcamp_attend(request: HttpRequest):
    """
    bootcamp参与率
    传入查询起始日期和结束日期
    """
    if request.method != "POST":
        return illegal_request_type_error_response()

    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return gen_response(400, "JSON format error")

    try:
        session = request.session
        role = session["role"]
    except KeyError:
        return session_timeout_response()

    if role not in ["admin", "HRBP"]:
        return unauthorized_action_response()

    try:
        startDate = data["dateRangeStart"]
        startDate = datetime.datetime.fromtimestamp(startDate / 1000)
        endDate = data["dateRangeEnd"]
        endDate = datetime.datetime.fromtimestamp(endDate / 1000)
    except KeyError:
        return gen_response(400, "JSON format error")

    if not (check_day(startDate, True) and check_day(endDate, False)):
        return gen_response(400, "Invalid date range")

    days = []
    totalEmploy = []
    school = []
    society = []
    intern = []
    unselect = []
    joinBootcamp = []
    for dayStart, dayEnd in date_ranges(startDate, endDate):
        users = PrivateInfo.objects.filter(joinDate__range = (dayStart, dayEnd))
        days.append(dayStart.date().isoformat()[5:])
        totalEmploy.append(users.count())
        school.append(users.filter(employeeType__exact = PrivateInfo.EnumEmployeeType.Campus).count())
        society.append(users.filter(employeeType__exact = PrivateInfo.EnumEmployeeType.Social).count())
        intern.append(users.filter(employeeType__exact = PrivateInfo.EnumEmployeeType.Intern).count())
        unselect.append(users.filter(employeeType__exact = PrivateInfo.EnumEmployeeType.Other).count())
        joinBootcamp.append(users.filter(isNew__exact = True).count())

    return gen_response(200, {
        "days": days,
        "totalEmploy": totalEmploy,
        "school": school,
        "society": society,
        "intern": intern,
        "unselect": unselect,
        "joinBootcamp": joinBootcamp,
    })


def newcomer_average_score(request: HttpRequest):
    """
    新人平均分
    """
    if request.method != "POST":
        return illegal_request_type_error_response()

    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return gen_response(400, "JSON format error")

    try:
        session = request.session
        role = session["role"]
        username = session["username"]
    except KeyError:
        return session_timeout_response()

    if role not in ["admin", "HRBP"]:
        return unauthorized_action_response()

    try:
        dept = PrivateInfo.objects.get(username = username).dept
    except Exception:
        return session_timeout_response()

    try:
        startDate = data["dateRangeStart"]
        startDate = datetime.datetime.fromtimestamp(startDate / 1000)
        endDate = data["dateRangeEnd"]
        endDate = datetime.datetime.fromtimestamp(endDate / 1000)
    except KeyError:
        return gen_response(400, "JSON format error")

    if not (check_day(startDate, True) and check_day(endDate, False)):
        return gen_response(400, "Invalid date range")

    users = PrivateInfo.objects.filter(newcomerGraduateDate__range = (startDate, endDate))

    return gen_response(200, {
        "group": average_score(users),
        "all": average_score(users.filter(dept__exact = dept)),
    })


def teacher_average_score(request: HttpRequest):
    """
    新人平均分
    """
    if request.method != "POST":
        return illegal_request_type_error_response()

    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return gen_response(400, "JSON format error")

    try:
        session = request.session
        role = session["role"]
        username = session["username"]
    except KeyError:
        return session_timeout_response()

    if role not in ["admin", "HRBP"]:
        return unauthorized_action_response()

    try:
        dept = PrivateInfo.objects.get(username = username).dept
    except Exception:
        return session_timeout_response()

    try:
        startDate = data["dateRangeStart"]
        startDate = datetime.datetime.fromtimestamp(startDate / 1000)
        endDate = data["dateRangeEnd"]
        endDate = datetime.datetime.fromtimestamp(endDate / 1000)
    except KeyError:
        return gen_response(400, "JSON format error")

    if not (check_day(startDate, True) and check_day(endDate, False)):
        return gen_response(400, "Invalid date range")

    users = PrivateInfo.objects.filter(teacherDutyDate__range = (startDate, endDate))

    return gen_response(200, {
        "group": average_score(users),
        "all": average_score(users.filter(dept__exact = dept)),
    })
