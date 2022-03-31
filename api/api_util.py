import re
from django.http import JsonResponse
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
    if len(PrivateInfo.objects.all().filter(username__exact=username)) == 0 \
            or not check_role_format(target_role):  # 用户不存在或查询的身份格式错误
        return False
    user_info = PrivateInfo.objects.all().filter(username__exact=username).first()  # 获取用户信息
    if target_role == "newcomer":  # 查询的身份是新人
        return user_info.isNew
    if target_role == "teacher":  # 查询的身份是导师
        return user_info.isTeacher
    if target_role.lower() == "hrbp":  # 查询的身份是hrbp
        return user_info.isHRBP
    if target_role == "admin":  # 查询的身份是管理员
        return user_info.isAdmin
    return False  # 这个分支不会被触发，出于鲁棒性考量返回一个False
