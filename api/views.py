# from django.shortcuts import render
"""
暂行的一部分接口文件,之后开始写接口后按接口分类进行文件划分
目前接口：Login登录，Join注册
"""
# Create your views here.


from django.http import JsonResponse
import json

def gen_response(code: int, data: str):
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def login(request): # 登录
    try:
        data = json.loads(request.body)
    except Exception as e:
        return gen_response(400, 'Load json request failed')
    
    # TODO: 在数据库中搜索用户、密码字段是否正确
    username = data.get('username')
    password = data.get('password')
    print(username, password) # 加密后的username和password
    return gen_response(200, { "result": "success", "message": "login successful" }) # 先暂时全部返回True


def join(request): # 注册
    try:
        data = json.loads(request.body)
    except Exception as e:
        return gen_response(400, 'Load json request failed')
    
    # TODO: 在数据库中搜索有没有重名的用户，如果没有则创建新用户
    username = data.get('username')
    password = data.get('password')
    personal_info = data.get('personal_info')
    print(username, password, personal_info) # 加密后的username和password，收到的个人信息（部门+城市）
    return gen_response(200, { "result": "success", "message": "registration successful" }) # 先暂时全部返回True
