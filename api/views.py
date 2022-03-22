"""
暂行的一部分接口文件,之后开始写接口后按接口分类进行文件划分
目前接口：Login登录，Join注册
"""
# from django.shortcuts import render
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import User


# Create your views here.

def test(request: HttpRequest):
    """
    for test
    :param request:
    :return:
    """
    if request.method == "GET":
        print("hello")
    user = User(name="hello")
    user.save()
    out = User.objects.all().first()
    return HttpResponse("ok,"+out.name)


def gen_response(code: int, data: str):
    '''
    for generating JsonResponse
    :param code, data
    :return JsonResponse
    '''
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def login(request):  # 登录
    '''
    recieve post '/login' from frontend
    request.body: username, password
    '''
    try:
        data = json.loads(request.body)
    except Exception:
        return gen_response(400, 'Load json request faile')

    # TODO: 在数据库中搜索用户、密码字段是否正确
    username = data.get('username')
    password = data.get('password')
    print(username, password)  # 加密后的username和password
    return_message = {"result": "success", "message": "login successful"}
    return gen_response(200, return_message)  # 先暂时全部返回True


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
    return_message = {"result": "success", "message": "registration successful"}
    return gen_response(200, return_message)  # 先暂时全部返回True
