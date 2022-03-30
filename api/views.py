"""
暂行的一部分接口文件,之后开始写接口后按接口分类进行文件划分
目前接口：Login登录，Join注册
"""
# from django.shortcuts import render
import json
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
        # 设置session信息并保存
        request.session['username'] = username  # 在session中保存username
        # TODO: 在身份系统实现之后引入身份的存储
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

    new_person = PrivateInfo.objects.create(name=personal_info["name"], dept=personal_info["department"],
                                            city=personal_info["city"], password=encrypt(password),
                                            username=username)
    new_person.save()
    # 设置session信息并保存
    request.session["username"] = username
    # TODO: 在身份系统实现之后引入身份的存储

    session_key = request.session.session_key
    return_message = "registration successful"
    response = JsonResponse({
        'code': 200,
        'data': return_message
    })
    response.set_cookie("SessionID", session_key)
    return gen_response(200, {}, message=return_message)  # 先暂时全部返回True
