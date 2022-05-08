import datetime
import logging
import re
from django.http import JsonResponse, HttpRequest
import hashlib
from .models import PrivateInfo, TeacherNewcomerTable, UserContentTable
from .models import ContentTable
import json

chinese_role_trans = {
    "admin": "管理员",
    "HRBP": "HRBP",
    "newcomer": "新人",
    "teacher": "导师"
}


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


def str_to_boolean(s: str):
    s = s.lower()
    if s == 'true':
        return True
    elif s == 'false':
        return False
    else:
        return None


def find_people(username: str):
    users = PrivateInfo.objects.filter(username=username)
    if len(users) <= 0:
        return False, gen_response(400, message=f"{username} user not found")
    else:
        return True, users.first()


def get_relation(teacher: str, newcomer: str):
    teachers = PrivateInfo.objects.filter(username=teacher)
    newcoemrs = PrivateInfo.objects.filter(username=newcomer)
    if len(teachers) <= 0 or len(newcoemrs) <= 0:
        return False, gen_response(400, message="teacher or newcomer not found")
    teacher = teachers.first()
    newcomer = newcoemrs.first()
    relations = TeacherNewcomerTable.objects.filter(teacher=teacher, newcomer=newcomer)
    if len(relations) <= 0:
        return False, gen_response(400, message="not relation between teacher and newcomer")
    return True, relations.first()


def quick_check(req: HttpRequest, check_points: dict):
    for key in check_points.keys():
        if key == "method" and not check_method(req, check_points[key]):
            # logging.error("invalid method")
            return False, gen_response(400, message="invalid method")
        elif key == "username":
            if req.session.get("username", None) is None:
                # logging.error("no username in session, probly not login")
                return False, gen_response(
                    400, message="no username in session, probly not login")
        elif key == "role" and not role_list_check(req.session.get("username"), check_points[key]):
            # logging.error("no permission")
            return False, gen_response(400, message="no permission")
        elif key == "data_field":
            try:
                data: dict = json.loads(req.body)
            except Exception:
                # logging.error("load fail")
                return False, gen_response(400, message='Load json request failed')
            for field in check_points[key]:
                if field not in data.keys():
                    # logging.error("lack of arguments")
                    return False, gen_response(400, message="lack of arguments")

    return True, gen_response(200)


def update_teacher_score(teacher:PrivateInfo):
    relations = TeacherNewcomerTable.objects.filter(teacher=teacher)
    count = 0
    total = 0
    for relation in relations:
        if relation.teacherScore >=0:
            count += 1
            total += relation.teacherScore
    teacher.teacherScore = total/count
    teacher.save()


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


def save_file_error_response():
    """
    生成保存文件错误响应
    """
    response: JsonResponse = JsonResponse({
        'result': 'failed',
        'message': 'failed to save file on server'
    })
    response.status_code = 400
    return response


def get_highest_role(username: str):
    """
    默认已经通过检查，则username必然存在，查询权限列表，返回最高权限的str
    :param username:
    :return: 最高权限str
    """
    p = PrivateInfo.objects.get(username=username)
    if p.isAdmin:
        return "admin"
    elif p.isHRBP:
        return "HRBP"
    elif p.isTeacher:
        return "teacher"
    else:
        return "newcomer"


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
    elif target_role == "teacher":  # 查询的身份是导师
        return user_info.isTeacher
    elif target_role.lower() == "hrbp":  # 查询的身份是hrbp
        return user_info.isHRBP
    elif target_role == "admin":  # 查询的身份是管理员
        return user_info.isAdmin
    else:
        return False


def get_role_list(username: str):
    try:
        user = PrivateInfo.objects.get(username__exact=username)
    except Exception as e:
        return []

    ret = []
    if user.isNew:
        ret.append("newcomer")
    if user.isTeacher:
        ret.append("teacher")
    if user.isHRBP:
        ret.append("HRBP")
    if user.isAdmin:
        ret.append("admin")

    return ret


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
        if role == "teacher" and info.isTeacher:
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
    info["department"] = pv.dept
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


def get_positions(pv: PrivateInfo) -> list:
    """
    返回具有权限的身份列表
    :param pv:
    :return: 身份列表
    """
    return_list = []
    if pv.isNew:
        return_list.append("新人")
    if pv.isTeacher:
        return_list.append("导师")
    if pv.isHRBP:
        return_list.append("HRBP")
    if pv.isAdmin:
        return_list.append("管理员")
    return return_list


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


def item_not_found_error_response():
    response: JsonResponse = JsonResponse({"result": "failure",
                                           "message": "requested item not found in database"})
    response.status_code = 400
    return response


def cn_datetime_fromtimestamp(timestamp: float) -> datetime.datetime:
    """
    将timestamp转换成datetime类（无时区信息的北京本地时间）
    如果你有上述需求，使用这个函数，而不是datetime.fromtimestamp

    P.S.
    我们构造的数据全是无时区信息的时间，所以要将USE_TZ设为False、且使用的datetime类也得是无时区的
    而python把时间戳转化为datetime时，是采用系统自身的时区信息进行转化的
    而服务器的时区信息是在芝加哥！！！
    如果直接使用datetime.fromtimestamp，部署上去的所有时间会延迟11个小时
    """
    local = datetime.datetime.now().replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
    beijing = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    delta = beijing - local
    return datetime.datetime.fromtimestamp(timestamp) + delta


def path_converter(path: str = input):
    return path.replace("\\", "/")


def get_progress(user: PrivateInfo, is_newcomer: bool = True, type:int = ContentTable.EnumType.Course ):
    """

    :param user:
    :param is_newcomer: True 为新人培训， False为导师培训
    :param type: 分别为EnumType.Course， EnumType.Exam，EnumType.Task
    :return:
    """
    if is_newcomer:
        audience = ContentTable.EnumAudience.newcomer
    else:
        audience = ContentTable.EnumAudience.teacher
    course = UserContentTable.objects.filter(
        user=user,
        content__audience=audience,
        content__type=type
    )
    if len(course) <= 0:
        return 100
    else:
        total_len = len(course)
        complete_len = len(course.filter(finished=True))
        return int(100*complete_len/total_len)


