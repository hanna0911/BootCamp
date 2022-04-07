"""
暂行的一部分接口文件,之后开始写接口后按接口分类进行文件划分
目前接口：Login登录，Join注册
"""
import datetime
import json
import logging
import django
import requests
from django.http import HttpRequest
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import PrivateInfo, UserProgramTable, ProgramTable
from .api_util import *


# Create your views here.
@ensure_csrf_cookie
def get_token(request: HttpRequest):
    if request.method == "GET":
        return gen_standard_response(200, {})
    else:  # 只接受GET请求
        return illegal_request_type_error_response()


def login(request: HttpRequest):  # 登录
    """
    receive post '/login' from frontend
    request.body: username, password
    保存相应的session信息用来完成登录的持久化
    """
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception:
        return gen_response(400, 'Load json request faile')

    # TODO: 在数据库中搜索用户、密码字段是否正确
    username = data.get('username')
    password = data.get('password')
    if "username" in request.session.keys():
        return gen_response(400, {}, "dup login")
    if len(PrivateInfo.objects.all().filter(username__exact=username)) == 0:
        return gen_response(400, {}, "user not found")
    elif PrivateInfo.objects.get(username__exact=username).password != encrypt(password):
        return gen_response(400, {}, "wrong password")
    else:
        # 设置session信息并保存 TODO: 在身份系统实现之后引入身份的存储
        request.session['username'] = username  # 在session中保存username
        # request.seesion['role'] = 'newcomer'  # 在session中保存当前身份，默认新人 TODO: 根据用户偏好设置默认身份,统一根据最高权级设置身份
        session_key = request.session.session_key
        # 返回成功信息
        # 返回成功信息
        return gen_set_cookie_response(code=200,
                                       data={"result": "success", "message": "account created"},
                                       cookie={"SessionID": session_key})


def join(request):  # 注册
    """
    recieve post '/join' from frontend
    request.body: username, password, personal_info
    """
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception:
        return gen_response(400, 'Load json request failed')

    # TODO: 在数据库中搜索有没有重名的用户，如果没有则创建新用户
    username = data.get('username')
    password = data.get('password')
    personal_info = data.get('personal_info')
    if not (username and password and personal_info):
        return gen_standard_response(code=400,
                                     data={"result": "failure", "message": 'lack of argument'})
    # 检查用户名格式
    if not check_username_format(username):
        return gen_standard_response(code=400,
                                     data={"result": "failure", "message": 'wrong username format'})
    elif not check_password_format(password):
        return gen_standard_response(code=400,
                                     data={"result": "failure", "message": 'wrong password format'})
    # 检查用户名重复
    if len(PrivateInfo.objects.all().filter(username__exact=username)) > 0:
        return gen_standard_response(code=400,
                                     data={"result": "failure", "message": 'duplicate username'})
    new_person = PrivateInfo(name=personal_info["name"], dept=personal_info["dept"],
                             city=personal_info["city"], password=encrypt(password),
                             username=username)
    # 身份系统测试： 默认有新人、导师和管理员三个身份， 没有hrbp
    new_person.isNew = True
    new_person.isAdmin = True
    new_person.isTeacher = True
    new_person.save()
    # 设置session信息并保存
    request.session["username"] = username
    request.session['role'] = 'newcomer'  # 在session中保存当前身份，默认新人 TODO: 根据用户偏好设置默认身份
    session_key = request.session.session_key
    # 返回成功信息
    return gen_set_cookie_response(code=200,
                                   data={"result": "success", "message": "account created"},
                                   cookie={"SessionID": session_key})


def switch_role(request: HttpRequest):
    """
    接收前端向/switch_role的post请求
    负载格式：{"action": "switch role", "switch_to": "newcomer/teacher/hrbp/admin"}
    更改当前身份
    """
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:
        request_data = json.loads(request.body)
    except Exception:  # json parse 失败
        return unknown_error_response()
    target_role = request_data.get('switch_to')
    if target_role is None:  # 字段缺失
        return gen_response(400, message="lack of arguments")
    user_session = request.session  # 获取session（根据cookie中的SessionID自动获取对应session）
    if user_session is None:  # session不存在
        return session_timeout_response()
    username = request.session["username"]

    if len(PrivateInfo.objects.all().filter(username__exact=username)) == 0:  # 数据库找不到这个用户
        logging.error("user not found")
        return gen_response(400, {}, "user not found")
    if not role_authentication(username=username, target_role=target_role):  # 用户没有此权限
        return gen_response(400, {}, "no permission or user not found ")
    # 验证成功则按下面的代码来处理
    user_session['role'] = target_role
    user_session.set_expiry(3600)  # session续命1小时
    logging.info(user_session['role'])
    return gen_standard_response(code=200,
                                 data={"result": "success",
                                       "message": 'role switched to ' + target_role})


def newcomer_info(request: HttpRequest):
    """
    接受前端向api/newcomer_info的post请求
    负载格式：{"action": "newcomer info", "newcomer": "__新人用户名__"}
    响应格式：{"result": "success", "message": "info for __新人用户名__ retrieved", "personal_info":{
            "name": "__新人姓名__",
            "city": "__新人城市__",
            "department": "__新人部门__",
            "username": "__新人用户名__",
            "bio": "__新人签名__",
            "join_date": "__新人入职时间__",
            "type": "__新人员工类型__",
            "manager": "__新人上级__",
            "details": "__新人入职情况详情__"},
            "programs": [{"program_id": "__项目id__",
                        "begin_time": "__开始时间__", "end_time": "__结束时间__",
                        "finished_content": __完成内容数__, "score": __分数__, deadline: "__项目ddl__"},
                        {}, ... , {}]}
    权限：admin, teacher
    """
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:  # 尝试parse请求中的json
        request_data = json.loads(request.body)
    except Exception:
        return gen_response(400, message="load json fail")
    target_username = request_data.get("newcomer")
    if target_username is None:
        return unknown_error_response()
    user_session = request.session  # 获取session（根据cookie中的SessionID自动获取对应session）
    if user_session is None or "role" not in user_session.keys():  # session不存在
        return session_timeout_response()
    if user_session["role"] != "admin" and user_session["role"] != "teacher":  # 权限认证
        return unauthorized_action_response()
    if len(PrivateInfo.objects.filter(username__exact=target_username)) == 0:  # 查找新人
        return gen_standard_response(400, {"result": "failure",
                                           "message": "newcomer not found"})
    # 获取个人信息
    newcomer = PrivateInfo.objects.filter(username__exact=target_username).first()
    program_relations = UserProgramTable.objects.filter(user=newcomer).all()
    response_data = {
        "result": "success",
        "message": f"info for {newcomer.username} retrieved",
        "personal_info": {
            "name": newcomer.name,
            "city": newcomer.city,
            "department": newcomer.dept,
            "username": newcomer.username,
            "bio": newcomer.bio,
            "join_date": str(newcomer.joinDate),
            "type": newcomer.employeeType,
            "manager": newcomer.leader,
            "details": newcomer.detail},
        "programs": []}
    # TODO: finish the user-program relation part of this function
    for relation in program_relations:
        response_data["programs"].append({
            "program_id": relation.program.id,
            "begin_time": str(relation.beginTime),
            "end_time": str(relation.endTime),
            "finished_content": relation.finishedContentCount,
            "score": relation.score,
            "deadline": str(relation.deadline)
        })
    print(response_data)
    return gen_standard_response(200, response_data)
