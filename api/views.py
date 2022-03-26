"""
暂行的一部分接口文件,之后开始写接口后按接口分类进行文件划分
目前接口：Login登录，Join注册
"""
# from django.shortcuts import render
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import PrivateInfo
import string
import re


# Create your views here.


def gen_response(code: int, data):
    """
    for generating JsonResponse
    :param code, data
    :return JsonResponse
    """
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def init_test(req: HttpRequest):
    """
    初始化测试
    """
    PrivateInfo.objects.get(username__exact="testid").delete()
    return gen_response(200, "ok")


def check_username_format(username: string):
    """
    用户名格式检测
    """
    if username is None:
        return False
    regex_result = re.search(r"\A[a-zA-Z0-9].{0,20}\Z", username)
    if regex_result is not None:
        return True
    else:
        return False


def check_password_format(password: string):
    """
    密码格式检测
    TODO: 把密码格式检测和SHA256加密从前端移到后端
    """
    if password is None:
        return False
    if not 8 <= len(password) <= 20:
        return False
    has_uppercase = re.search(r"[A-Z]+", password)  # 判断是否含有大写字母
    has_lowercase = re.search(r"[a-z]+", password)  # 判断是否含有小写字母
    has_number = re.search(r"[0-9]+", password)  # 判断是否含有数字
    has_special_char = re.search(r"(?=[^A-Za-z0-9)])(?=[\S]).{1}")  # 判断是否含有特殊字符
    if has_uppercase and has_lowercase and has_number and has_special_char:
        return True
    else:
        return False


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
        return gen_response(400, {"result": "failure", "message": "user not found"})
    elif PrivateInfo.objects.all().filter(username__exact=username).first().password != password:
        return gen_response(400, {"result": "failure", "message": "wrong password"})
    else:
        print(username, password)  # 加密后的username和password
        # 设置session信息并保存
        request.session['username'] = username  # 在session中保存username
        # TODO: 在身份系统实现之后引入身份的存储
        session_key = request.session.session_key
        # 返回成功信息
        return_message = {"result": "success", "message": "login successful"}
        response = JsonResponse({
            'code': 200,
            'data': return_message
        })
        response.set_cookie("SessionID", session_key)
        return response


def join(request):  # 注册
    '''
    recieve post '/join' from frontend
    request.body: username, password, personal_info
    '''
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
        return gen_response(400, {"result": "failure", "message": "wrong username format"})
    # 检查用户名重复
    if len(PrivateInfo.objects.all().filter(username__exact=username)) > 0:
        return gen_response(400, {"result": "failure", "message": "duplicate username"})

    new_person = PrivateInfo(name=personal_info["name"], dept=personal_info["department"],
                             city=personal_info["city"], password=password, username=username)
    new_person.save()

    # 设置session信息并保存
    request.session["username"] = username
    # TODO: 在身份系统实现之后引入身份的存储

    session_key = request.session.session_key
    print(check_username_format(username))
    return_message = {"result": "success", "message": "registration successful"}
    response = JsonResponse({
        'code': 200,
        'data': return_message
    })
    response.set_cookie("SessionID", session_key)
    return response  # 先暂时全部返回True
