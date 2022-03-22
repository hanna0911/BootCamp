'''
just for test: 只是用来测试前后端Login通信，后期请单独建app来写views.py（不要写在根目录里）
'''

from django.http import HttpResponse, JsonResponse
import json

def gen_response(code: int, data: str):
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def login(request):
    try:
        data = json.loads(request.body)
    except Exception as e:
        return gen_response(400, 'Load json request failed')
    
    # TODO: 在数据库中搜索用户、密码字段是否正确
    username = data.get('username')
    password = data.get('password')
    print(username, password) # 加密后的username和password
    return gen_response(200, { "result": "success", "message": "login successful" }) # 先暂时全部返回True


def join(request):
    try:
        data = json.loads(request.body)
    except Exception as e:
        return gen_response(400, 'Load json request failed')
    
    # TODO: 在数据库中搜索有没有重名的用户，如果没有则创建新用户
    username = data.get('username')
    password = data.get('password')
    personal_info = data.get('personal_info')
    print(username, password, personal_info) # 加密后的username和password
    return gen_response(200, { "result": "success", "message": "registration successful" }) # 先暂时全部返回True
