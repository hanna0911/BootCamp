"""
数据分析相关的api接口
"""

from datetime import datetime
from json import JSONDecodeError
import logging
from django.http import HttpRequest
from .api_util import *
from .models import *


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

    if not role in ["admin", "HRBP"]:
        return unauthorized_action_response()

    try:
        startDate = data["dateRangeStart"]
        startDate = datetime.fromtimestamp(startDate / 1000)
        endDate = data["dateRangeEnd"]
        endDate = datetime.fromtimestamp(endDate / 1000)
    except KeyError:
        return gen_response(400, "JSON format error")

    users = PrivateInfo.objects.filter(joinDate__range = (startDate, endDate))
    return gen_response(200, "JSON format error")