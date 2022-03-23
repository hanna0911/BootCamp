"""
暂行的一部分接口文件,之后开始写接口后按接口分类进行文件划分
目前接口：Login登录，Join注册
"""
# from django.shortcuts import render
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import PrivateInfo


# Create your views here.


def gen_response(code: int, data):
    '''
    for generating JsonResponse
    :param code, data
    :return JsonResponse
    '''
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def login(request: HttpRequest):  # 登录
    '''
    recieve post '/login' from frontend
    request.body: username, password
    '''
    try:
        data = json.loads(request.body)
        print(data)
    except Exception:
        return gen_response(400, 'Load json request faile')

    # TODO: 在数据库中搜索用户、密码字段是否正确
    username = data.get('username')
    password = data.get('password')
    if len(PrivateInfo.objects.all().filter(userid__exact=username)) == 0:
        return gen_response(400, {"result": "failure", "message": "user not found"})
    elif PrivateInfo.objects.all().filter(userid__exact=username).first().password != password:
        return gen_response(400, {"result": "failure", "message": "wrong password"})
    else:
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
    # 检查用户名重复
    if len(PrivateInfo.objects.all().filter(userid__exact=username)) > 0:
        return gen_response(400, {"result": "failure", "message": "duplicate username"})
    new_person = PrivateInfo(name=personal_info["name"], dept=personal_info["department"],
                             city=personal_info["city"], password=password, userid=username)
    new_person.save()
    return_message = {"result": "success", "message": "registration successful"}
    return gen_response(200, return_message)  # 先暂时全部返回True
