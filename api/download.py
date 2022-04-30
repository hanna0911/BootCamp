"""
下载相关接口
"""
from django.http import HttpRequest, StreamingHttpResponse, HttpResponse
from wsgiref.util import FileWrapper
import re
import os
import mimetypes
import csv
import json
from api.models import ContentTable, PrivateInfo, UserContentTable
from api.api_util import *
from api.upload import parse_test_for_grader, parse_test_for_student, grade_test


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data


def stream_video(request: HttpRequest):
    """将视频文件以流媒体的方式响应"""
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    path = request.GET.get('path')
    # 这里根据实际情况改变，我的views.py在core文件夹下但是folder_path却只到core的上一层，media也在core文件夹下
    folder_path = os.getcwd().replace('\\', '/')
    print(folder_path)
    path = folder_path + '/static/' + path  # path就是template ？后面的参数的值
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 10
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206,
                                     content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    resp.status_code = 200
    return resp


def retrieve_test_info_by_id(request: HttpRequest):
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception:
        return gen_response(400, 'Load json request failed')
    user_session = request.session
    if user_session is None or "role" not in user_session.keys():  # session不存在
        return session_timeout_response()
    action = data.get("action")
    test_content_id = data.get("testID")
    if action is None or action != "retrieve test info"\
       or test_content_id is None:
        return gen_standard_response(400, {"result": "failure", "message": "Bad Arguments"})
    if len(ContentTable.objects.filter(id=test_content_id)) == 0:
        return item_not_found_error_response()
    test = ContentTable.objects.filter(id=test_content_id).first()
    print(test.type)
    if test.type != 1:
        return item_not_found_error_response()
    return gen_standard_response(200, {
        "name": test.name,
        "intro": test.intro,
        "time": test.recommendedTime,
        "tag": test.tag,
        "author": test.author.name
    })


def retrieve_test_paper_by_id(request: HttpRequest):
    """
    文件功能测试接口
    接收POST请求
    格式：{action: "retrieve test paper", testID: __CONTENT_ID__}
    """
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception:
        return gen_response(400, 'Load json request failed')
    user_session = request.session
    if user_session is None or "role" not in user_session.keys():  # session不存在
        return session_timeout_response()
    action = data.get("action")
    test_content_id = data.get("testID")
    if action is None or action != "retrieve test paper"\
       or test_content_id is None:
        return gen_standard_response(400, {"result": "failure", "message": "Bad Arguments"})
    if len(ContentTable.objects.filter(id=test_content_id)) == 0:
        return item_not_found_error_response()
    test = ContentTable.objects.filter(id=test_content_id).first()
    if test.type != 1:
        return item_not_found_error_response()
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=test_paper.csv'
    try:
        fp = open(test.questions, "r", encoding="UTF-8")
    except Exception as e:
        print(e)
        return item_not_found_error_response()
    csv_reader = csv.reader(fp)
    csv_writer = csv.writer(response)
    csv_writer.writerows(csv_reader)
    response.status_code = 200
    return response


def retrieve_test_by_user_id(request: HttpRequest):
    """
    文件功能正式接口
    接收POST请求
    {action: "retrieve tests by user id", "username": __USER_ID__}
    """
    if request.method != 'action':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    session = request.session
    action = data.get('action')
    target_username = data.get('username')
    if action != 'retrieve tests by user id' or target_username is None:
        return gen_standard_response(400, {"result": "failed", "message": "Bad Arguments"})
    target_user_filter = PrivateInfo.objects.filter(username=target_username)
    if len(target_user_filter) == 0:
        return item_not_found_error_response()
    target_user = target_user_filter.first()
    target_tests = UserContentTable.objects.filter(user=target_user, content__type=ContentTable.EnumType.Exam)
    test_list = []
    for test_relation in target_tests:
        test = test_relation.content
        if test.audience == 0:
            audience = 'newcomer'
        else:
            audience = 'teacher'
        test_info = [
            audience,
            test.isTemplate,
            test.name,
            test.intro,
            test.recommendedTime,
            test.tag,
            test.author.name,
            test.releaseTime
        ]
        try:
            fp = open(test.questions, "r", encoding="UTF-8")
        except Exception as e:
            print(e)
            return item_not_found_error_response()
        test_paper = parse_test_for_student(test.questions)
        test_list.append([test_info, test_paper])
    return gen_standard_response(200, {"result": "success",
                                       "message": f"tests retrieved for {target_username}",
                                       "tests": test_list})
