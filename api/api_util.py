import re
from django.http import JsonResponse
import hashlib
from .models import PrivateInfo


def gen_response(code: int, data, message="succeed"):
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
    encoder = hashlib.sha256()
    encoder.update(cleartext)
    ret = encoder.hexdigest()
    return ret


def get_permission(username: str):
    """
    获取该用户的所有权限
    :param username: 用户名
    :return:
    """
    person = PrivateInfo.objects.all().get(username__exact=username)
    if person:
        return person.isNew, person.isTeacher, person.isHRBP, person.isAdmin
    else:
        raise Exception("找不到username:{}".format(username))


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
