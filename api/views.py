"""
暂行的一部分接口文件,之后开始写接口后按接口分类进行文件划分
目前接口：Login登录，Join注册
"""
# from django.shortcuts import render
import datetime
import json

import requests
from django.http import HttpRequest
from .models import PrivateInfo
from .api_util import *


# Create your views here.


def login(request: HttpRequest):  # 登录
    """
    receive post '/login' from frontend
    request.body: username, password
    保存相应的session信息用来完成登录的持久化
    """
    try:
        data = json.loads(request.body)
        print(data)
    except Exception:
        return gen_response(400, 'Load json request faile')

    # TODO: 在数据库中搜索用户、密码字段是否正确
    username = data.get('username')
    password = data.get('password')
    if len(PrivateInfo.objects.all().filter(username__exact=username)) == 0:
        return gen_response(400, {}, "user not found")
    elif PrivateInfo.objects.get(username__exact=username).password != encrypt(password):
        return gen_response(400, {}, "wrong password")
    else:
        print(username, password)  # 加密后的username和password
        # 设置session信息并保存 TODO: 在身份系统实现之后引入身份的存储
        request.session['username'] = username  # 在session中保存username
        print(request.session['role'])
        # request.seesion['role'] = 'newcomer'  # 在session中保存当前身份，默认新人 TODO: 根据用户偏好设置默认身份
        session_key = request.session.session_key
        # 返回成功信息
        response = JsonResponse({
            'code': 200,
            'data': {},
            "message": "login successful"
        })
        response.set_cookie("SessionID", session_key)
        return response


def join(request):  # 注册
    """
    recieve post '/join' from frontend
    request.body: username, password, personal_info
    """
    try:
        data = json.loads(request.body)
    except Exception:
        print(0)
        return gen_response(400, 'Load json request failed')

    # TODO: 在数据库中搜索有没有重名的用户，如果没有则创建新用户
    username = data.get('username')
    password = data.get('password')
    personal_info = data.get('personal_info')
    print(username, password, personal_info)  # 加密后的用户名、密码，收到的个人信息（部门+城市）

    # 检查用户名格式
    if not check_username_format(username):
        return gen_response(400, {}, "wrong username format")
    elif not check_password_format(password):
        return gen_response(400, {}, "wrong password format")
    # 检查用户名重复
    if len(PrivateInfo.objects.all().filter(username__exact=username)) > 0:
        return gen_response(400, {}, "duplicate username")

    new_person = PrivateInfo(name=personal_info["name"], dept=personal_info["department"],
                                            city=personal_info["city"], password=encrypt(password),
                                            username=username)
    # 身份系统测试： 默认有新人、导师和管理员三个身份， 没有hrbp
    # new_person.isNew = True
    # new_person.isAdmin = True
    # new_person.isTeacher = True
    new_person.save()
    # 设置session信息并保存
    request.session["username"] = username
    request.session['role'] = 'newcomer'  # 在session中保存当前身份，默认新人 TODO: 根据用户偏好设置默认身份
    session_key = request.session.session_key
    # 返回成功信息
    return_message = "registration successful"
    response = JsonResponse({
        'code': 200,
        'data': return_message
    })
    response.set_cookie("SessionID", session_key)
    return response  # 先暂时全部返回True


def switch_role(request: HttpRequest):
    """
    接收前端向/switch_role的post请求
    负载格式：{"action": "switch role", "switch_to": "newcomer/teacher/hrbp/admin"}
    更改当前身份
    """
    try:
        request_data = json.loads(request.body)
    except Exception:  # json parse 失败
        return unknown_error_response()
    action = request_data.get('action')
    target_role = request_data.get('switch_to')
    print(action, target_role)
    if action is None or action != "switch role" or target_role is None:  # 字段缺失或action字段错误
        return unknown_error_response()
    if not check_username_format(target_role):  # switch_to字段错误
        return unknown_error_response()
    user_session = request.session  # 获取session（根据cookie中的SessionID自动获取对应session）
    if user_session is None:  # session不存在
        return session_timeout_response()

    username = user_session['username']
    if len(PrivateInfo.objects.all().filter(username__exact=username)) == 0:  # 数据库找不到这个用户
        return unknown_error_response()
    if not role_authentication(username=username, target_role=target_role):  # 用户没有此权限
        return unknown_error_response()
    # 验证成功则按下面的代码来处理
    user_session['role'] = target_role
    user_session.set_expiry(3600)  # session续命1小时
    response: JsonResponse = JsonResponse({
        'result': 'success',
        'message': 'role switched to ' + target_role
    })
    response.status_code = 200
    print(request.session['role'])
    return response


def admin_newcomer_list(request: HttpRequest):
    """
    接收前端向/admin_newcomer_list的get请求
    获取所有新人的数据
    仅限管理员使用
    TODO
    """


def newcomer_info(request: HttpRequest):
    """
    接受前端向/newcomer_info的post请求
    TODO
    """
