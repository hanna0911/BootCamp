import re
from django.http import JsonResponse, HttpRequest
import hashlib
from .models import PrivateInfo


def gen_response(code: int, data={}, message="succeed"):
    """
    for generating JsonResponse
    :param code, data
    :return JsonResponse
    """
    return JsonResponse({
        'code': code,
        'data': data,
        'message': message
    }, status=code)


def encrypt(cleartext: str):
    """
    SHA256 Encryption Function
    """
    cleartext = str(cleartext).encode('utf-8')
    encoder = hashlib.sha256()
    encoder.update(cleartext)
    ret = encoder.hexdigest()
    return ret


def check_username_format(username: str):
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


def check_password_format(password: str):
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
    has_special_char = re.search(r"(?=[^A-Za-z0-9)])(?=[\S]).{1}", password)  # 判断是否含有特殊字符
    if has_uppercase and has_lowercase and has_number and has_special_char:
        return True
    else:
        return False


def check_role_format(role: str):
    """
    身份名称合法性校验
    仅 newcomer, teacher, hrbp, admin 合法
    """
    if role == "newcomer" or role == "teacher" or role.lower() == "hrbp" or role == "admin":
        return True
    else:
        raise Exception("invalid role format")


def check_method(req: HttpRequest, method: str):
    if req.method == method.upper():
        return True
    else:
        return False


def unknown_error_response():
    """
    生成未知错误的标准响应
    """
    response: JsonResponse = JsonResponse({
        'result': 'failed',
        'message': 'unknown error'
    })
    response.status_code = 400
    return response


def session_timeout_response():
    """
    生成session不存在或超时的标准响应
    """
    response: JsonResponse = JsonResponse({
        'result': 'failed',
        'message': 'sessions timeout'
    })
    response.status_code = 400
    return response


def unauthorized_action_response():
    """
    生成无权限错误的标准响应
    """
    response: JsonResponse = JsonResponse({
        'result': 'failed',
        'message': 'unauthorized action'
    })
    response.status_code = 400
    return response


def role_authentication(username: str, target_role: str):
    """
    校验某用户是否具有某身份的权限
    """
    check_role_format(target_role)
    if len(PrivateInfo.objects.all().filter(username__exact=username)) == 0:  # 用户不存在或查询的身份格式错误
        return False
    user_info = PrivateInfo.objects.get(username__exact=username)  # 获取用户信息
    if target_role == "newcomer":  # 查询的身份是新人
        return user_info.isNew
    if target_role == "teacher":  # 查询的身份是导师
        return user_info.isTeacher
    if target_role.lower() == "hrbp":  # 查询的身份是hrbp
        return user_info.isHRBP
    if target_role == "admin":  # 查询的身份是管理员
        return user_info.isAdmin


def role_list_check(username: str, rolelist: list):
    if len(PrivateInfo.objects.filter(username=username)) == 0:
        return False
    info = PrivateInfo.objects.get(username=username)
    for role in rolelist:
        check_role_format(role)
        if role == "newcomer" and info.isNew:
            return True
        if role == "admin" and info.isAdmin:
            return True
        if role.lower() == "hrbp" and info.isHRBP:
            return True
        if role == " teacher" and info.isTeacher:
            return True
    return False


def load_private_info(pv: PrivateInfo) -> dict:
    """
    只load 个人信息部分，新人和导师信息需要根据不同接口分别写入
    :param pv:
    :return:
    """
    info = {}
    info["username"] = pv.username
    info["name"] = pv.name
    info["city"] = pv.city
    info["dept"] = pv.dept
    info["bio"] = pv.bio

    info["joinDate"] = pv.joinDate
    if pv.joinStatus == 0:
        info["joinStatus"] = "待入职"
        info["employed"] = "待入职"
    elif pv.joinStatus == 1:
        info["joinStatus"] = "在职"
        info["employed"] = "在职"
    elif pv.joinStatus == 2:
        info["joinStatus"] = "离职"
        info["employed"] = "离职"
    else:
        info["joinStatus"] = "未知"
        info["employed"] = "未知"
    info["detail"] = pv.detail
    info["leader"] = pv.leader
    info["superior"] = pv.leader  # temp
    info["registrationDate"] = pv.registrationDate
    info["employeeType"] = pv.employeeType

    info["isAdmin"] = pv.isAdmin
    info["isTeacher"] = pv.isTeacher
    info["isHRBP"] = pv.isHRBP
    info["isNew"] = pv.isNew
    return info


def gen_set_cookie_response(code: int, data: dict = {}, cookie: dict = {}):
    """
    生成带有set-cookie的response
    P.S. 不要乱改已经写好的response！以及不要和接口文档有任何出入！
    """
    response: JsonResponse = JsonResponse(data)
    response.status_code = code
    for key in cookie.keys():
        response.set_cookie(key, cookie[key])
    return response


def gen_standard_response(code: int, data: dict = {}):
    response: JsonResponse = JsonResponse(data)
    response.status_code = code
    return response


def illegal_request_type_error_response():
    response: JsonResponse = JsonResponse({"result": "error",
                                           "message": "illegal request type"})
    response.status_code = 400
    return response
