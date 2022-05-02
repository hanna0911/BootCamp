import json
import logging
import sys

from django.http import HttpRequest
from platformdirs import os
from .api_util import *
from .models import *
from .upload import parse_test_for_student, parse_test_for_admin


def admin_newcomer_list(request: HttpRequest):
    """
    接收前端向/admin_newcomer_list的get请求
    获取所有新人的数据
    仅限管理员使用
    TODO
    """
    if not check_method(request, "GET"):
        return gen_response(400, message="invalid method")
    username = request.session.get("username", None)
    if username is None:
        return gen_response(400, message="no username in session, probly not login")
    if not role_authentication(username, "admin"):
        return gen_response(400, message="permission deny")

    newcomer_list = PrivateInfo.objects.filter(isNew=True, isTeacher=False, isAdmin=False, isHRBP=False)
    return_list = []
    for newcomer in newcomer_list:
        tmp = load_private_info(newcomer)
        teacher_queue = TeacherNewcomerTable.objects.filter(newcomer=newcomer)
        if len(teacher_queue) == 0:
            tmp["tutor"] = "无"
            tmp["teacher"] = "无"
        else:
            tmp["teacher"] = teacher_queue.first().teacher.name
            tmp["tutor"] = teacher_queue.first().teacher.name
        tmp["joinBootcamp"] = True
        tmp["graduated"] = newcomer.newcomerGraduateState  # temp
        tmp["evaluate"] = "暂无"
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(newcomer.username)  # 直接后端指定路径，前端自动请求
        return_list.append(tmp)
    return gen_response(200, return_list, "tmp supported")


def teacher_wait_list(req: HttpRequest):
    """
    权限确认(admin)
    筛选出导师候选人(已经完成新人培训的新人),返回基本信息列表
    :param req:
    :return:
    """
    if not check_method(req, "GET"):
        return gen_response(400, message="invalid method")
    username = req.session.get("username", None)
    if username is None:
        return gen_response(
            400, message="no username in session, probly not login")
    if not role_authentication(username, 'admin'):
        return gen_response(400, message="no permission")
    newcommer_list = PrivateInfo.objects.filter(isTeacher=False, isNew=True)
    return_list = []
    for new in newcommer_list:
        tmp = load_private_info(new)
        return_list.append(tmp)
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(new.username)
    return gen_response(200, return_list)


def nominate_process(req: HttpRequest):
    """
    提名进度列表
    :param req:
    :return:
    """
    username = req.session.get("username", None)
    if not check_method(req, "GET"):
        return gen_response(400, message="invalid method")
    if username is None:
        return gen_response(
            400, message="no username in session, probly not login")
    if not role_authentication(username, 'admin'):
        return gen_response(400, message="no permission")
    teacher_list = PrivateInfo.objects.filter(isTeacher=True, teacherIsDuty=False)
    return_list = []
    for teacher in teacher_list:
        tmp = load_private_info(teacher)
        tmp["teacherNominationDate"] = teacher.teacherNominationDate
        status = teacher.teacherExaminedStatus
        if status == PrivateInfo.EnumTeacherExaminedStatus.NotYet:
            tmp["teacherExaminedStatus"] = "未审核"
        elif status == PrivateInfo.EnumTeacherExaminedStatus.Pass:
            tmp["teacherExaminedStatus"] = "通过"
        elif status == PrivateInfo.EnumTeacherExaminedStatus.Fail:
            tmp["teacherExaminedStatus"] = "拒绝"
        else:
            raise Exception("数据可数据错误，请检查写入接口是否正确")
        user_program = teacher.ProgramsAsUser.filter(program__audience=1).first()
        if user_program is None:
            tmp["learningStatus"] = "未参加"
        elif user_program.finished:
            tmp["learningStatus"] = "已完成"
        else:
            tmp["learningStatus"] = "进行中"
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(teacher.username)
        return_list.append(tmp)
    return gen_response(200, return_list, "send {} data".format(len(return_list)))


def duty_teacher_list(req: HttpRequest):
    if not check_method(req, "GET"):
        return gen_response(400, message="invalid method")
    username = req.session.get("username", None)
    if username is None:
        return gen_response(
            400, message="no username in session, probly not login")
    if not role_list_check(username, ["admin", "HRBP"]):
        return gen_response(400, message="permission denied")
    teacher_list = PrivateInfo.objects.filter(isTeacher=True, teacherIsDuty=True)
    return_list = []
    for teacher in teacher_list:
        tmp = load_private_info(teacher)
        tmp["historicalMembers"] = teacher.historicalMembers
        tmp["currentMembers"] = teacher.currentMembers
        tmp["teacherDutyDate"] = teacher.teacherDutyDate
        tmp["teacherScore"] = teacher.teacherScore
        tmp["OKR"] = "unknown"
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(teacher.username)
        return_list.append(tmp)
    return gen_response(200, data=return_list, message="send {} data".format(len(return_list)))


def nominated_list(req: HttpRequest):
    """
    已经被提名,可以进行审核的教室列表
    :param req:
    :return:
    """
    if not check_method(req, "GET"):
        return gen_response(400, message="invalid method")
    username = req.session.get("username", None)
    if username is None:
        return gen_response(
            400, message="no username in session, probly not login")
    if not role_list_check(username, ["HRBP", "admin"]):  # 暂时做修改适应前端
        return gen_response(400, message="permission denied")
    teacher_list = PrivateInfo.objects.filter(isTeacher=True, teacherIsDuty=False)
    # TODO:获取培训状态
    return_list = []
    for teacher in teacher_list:
        tmp = load_private_info(teacher)
        tmp["teacherNominationDate"] = teacher.teacherNominationDate
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(teacher.username)
        return_list.append(tmp)
    return gen_response(200, data=return_list)


def assignable_test_list(request: HttpRequest):
    """
    获取一个用户自己可给他人分配的所有考试
    """
    if request.method != 'GET':
        return illegal_request_type_error_response()
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if username is None or role is None:
        return session_timeout_response()
    if role == 'admin':
        available_tests = ContentTable.objects.filter(type=ContentTable.EnumType.Exam)
        test_list = []
        recommend_time_list = []
        tag_list = []
        for test in available_tests:
            if test.audience == 0:
                audience = 'newcomer'
            else:
                audience = 'teacher'
            test_info = {
                'audience': audience,
                'is_template': test.isTemplate,
                'name': test.name,
                'intro': test.intro,
                'recommend_time': str(test.recommendedTime),
                'tag': test.tag,
                'author_name': test.author.name,
                'releaseTime': test.releaseTime,
                'testID': test.id,
            }
            recommend_time_list.append(str(test.recommendedTime))
            tag_list.append(test.tag)
            try:
                # if test.questions == '' or test.questions is None:
                #     csv_dir = './files/test/SampleTestPaper.csv'
                # else:
                #     csv_dir = test.questions
                csv_dir = test.questions
                fp = open(csv_dir, "r", encoding="UTF-8")
            except Exception as e:
                print(e)
                return item_not_found_error_response()
            print(csv_dir)
            test_paper = parse_test_for_admin(csv_dir)
            test_list.append({'test_info': test_info, 'test_paper': test_paper, 'courseDialog': False})
        print(test_list)
        recommend_time_list = list(set(recommend_time_list))
        tag_list = list(set(tag_list))
        return gen_standard_response(200, {'result': 'success',
                                           'message': f'assignable tests retrieved for admin user {username}',
                                           'tests': test_list, 'test_recommend_time_items': recommend_time_list, 'test_tag_items': tag_list})
    elif role == 'teacher':
        test_templates = ContentTable.objects.filter(isTemplate=True,
                                                     audience=0,
                                                     type=ContentTable.EnumType.Exam)
        authored_tests = ContentTable.objects.filter(author__username=username,
                                                     audience=0,
                                                     type=ContentTable.EnumType.Exam,
                                                     isTemplate=False)
        available_tests = test_templates.union(authored_tests)
        test_list = []
        for test in available_tests:
            if test.audience == 0:
                audience = 'newcomer'
            else:
                audience = 'teacher'
            test_info = {
                'audience': audience,
                'isTemplate': test.isTemplate,
                'name': test.name,
                'intro': test.intro,
                'recommendedTime': test.recommendedTime,
                'tag': test.tag,
                'author_name': test.author.name,
                'releaseTime': test.releaseTime,
                'testID': test.id,
            }
            try:
                # if test.questions == '' or test.questions is None:
                #     csv_dir = './files/test/SampleTestPaper.csv'
                # else:
                #     csv_dir = test.questions
                csv_dir = test.questions
                fp = open(csv_dir, "r", encoding="UTF-8")
            except Exception as e:
                print(e)
                return item_not_found_error_response()
            test_paper = parse_test_for_admin(csv_dir)
            test_list.append({'test_info': test_info, 'test_paper': test_paper})
        print(test_list)
        return gen_standard_response(200, {'result': 'success',
                                           'message': f'assignable tests retrieved for teacher user {username}',
                                           'tests': test_list})
    elif role == 'HRBP':
        test_templates = ContentTable.objects.filter(isTemplate=True,
                                                     audience=1,
                                                     type=ContentTable.EnumType.Exam)
        authored_tests = ContentTable.objects.filter(author__username=username,
                                                     audience=1,
                                                     type=ContentTable.EnumType.Exam,
                                                     isTemplate=False)
        available_tests = test_templates.union(authored_tests)
        test_list = []
        for test in available_tests:
            if test.audience == 0:
                audience = 'newcomer'
            else:
                audience = 'teacher'
            test_info = {
                'audience': audience,
                'isTemplate': test.isTemplate,
                'name': test.name,
                'intro': test.intro,
                'recommendedTime': test.recommendedTime,
                'tag': test.tag,
                'author_name': test.author.name,
                'releaseTime': test.releaseTime,
                'testID': test.id,
            }
            try:
                # if test.questions == '' or test.questions is None:
                #     csv_dir = './files/test/SampleTestPaper.csv'
                # else:
                #     csv_dir = test.questions
                csv_dir = test.questions
                fp = open(csv_dir, "r", encoding="UTF-8")
            except Exception as e:
                print(e)
                return item_not_found_error_response()
            test_paper = parse_test_for_admin(csv_dir)
            test_list.append({'test_info': test_info, 'test_paper': test_paper})
        print(test_list)
        return gen_standard_response(200, {'result': 'success',
                                           'message': f'assignable tests retrieved for hrbp user {username}',
                                           'tests': test_list})
    else:  # newcomer
        return unauthorized_action_response()


def my_test_list(request: HttpRequest):
    """
    获取一个用户要参加的全部考试
    """
    if request.method != 'GET':
        return illegal_request_type_error_response()
    session = request.session
    username = session.get('username')
    role = session.get('role')
    print('my_test_list session:', username, role)
    if username is None or role is None:
        return session_timeout_response()
    if role != 'teacher' and role != 'newcomer':
        return unauthorized_action_response()
    target_tests = UserContentTable.objects.filter(user__username=username, content__type=ContentTable.EnumType.Exam)
    test_list = []
    for test_relation in target_tests:
        test = test_relation.content
        if test.audience == 0:
            audience = 'newcomer'
        else:
            audience = 'teacher'
        test_info = {
            'audience': audience,
            'isTemplate': test.isTemplate,
            'name': test.name,
            'intro': test.intro,
            'recommendedTime': test.recommendedTime,
            'tag': test.tag,
            'author_name': test.author.name,
            'releaseTime': test.releaseTime,
            'testID': test.id,
        }
        try:
            # if test.questions == '' or test.questions is None:
            #     csv_dir = './files/test/SampleTestPaper.csv'
            # else:
            #     csv_dir = test.questions
            csv_dir = test.questions
            fp = open(csv_dir, "r", encoding="UTF-8")
        except Exception as e:
            print(e)
            return item_not_found_error_response()
        test_paper = parse_test_for_student(csv_dir)
        test_list.append({'test_info': test_info, 'test_paper': test_paper})
    print(test_list)
    return gen_standard_response(200, {"result": "success",
                                       "message": f'my tests retrieved for {role} user {username}',
                                       "tests": test_list})


def assignable_course_list(request: HttpRequest):
    """
    获取一个用户可分配给其他用户的全部课程
    """
    if request.method != 'GET':
        return illegal_request_type_error_response()
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if username is None or role is None:
        return session_timeout_response()
    course_list = []
    if role == 'admin':
        available_courses = ContentTable.objects.filter(type=ContentTable.EnumType.Course)
    elif role == 'teacher':
        course_templates = ContentTable.objects.filter(type=ContentTable.EnumType.Course,
                                                       isTemplate=True,
                                                       audience=0)
        authored_courses = ContentTable.objects.filter(type=ContentTable.EnumType.Course,
                                                       isTemplate=False,
                                                       audience=0,
                                                       author__username=username)
        available_courses = course_templates.union(authored_courses)
    elif role == 'HRBP':
        course_templates = ContentTable.objects.filter(type=ContentTable.EnumType.Course,
                                                       isTemplate=True,
                                                       audience=1)
        authored_courses = ContentTable.objects.filter(type=ContentTable.EnumType.Course,
                                                       isTemplate=False,
                                                       audience=1,
                                                       author__username=username)
        available_courses = course_templates.union(authored_courses)
    else:  # newcomer
        return unauthorized_action_response()
    for course in available_courses:
        if course.audience == 0:
            audience = 'newcomer'
        else:
            audience = 'teacher'
        course_list.append([
            audience,
            course.isTemplate,
            course.name,
            course.intro,
            course.recommendedTime,
            course.tag,
            course.author.name,
            course.releaseTime,
            course.lessonCount,
        ])
    return gen_standard_response(200, {'result': 'success',
                                       'message': f'assignable courses retrieved for {role} user {username}',
                                       'courses': course_list})


def my_courses_list(request: HttpRequest):
    """
    获取一个用户可以学习的全部课程
    """
    if request.method != 'GET':
        return illegal_request_type_error_response()
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if username is None or role is None:
        return session_timeout_response()
    if role != 'teacher' and role != 'newcomer':
        return unauthorized_action_response()
    target_courses = UserContentTable.objects.filter(user__username=username, content__type=ContentTable.EnumType.Course)
    course_list = []
    for course_relation in target_courses:
        course = course_relation.content
        if course.audience == 0:
            audience = 'newcomer'
        else:
            audience = 'teacher'
        course_list.append([
            audience,
            course.isTemplate,
            course.name,
            course.intro,
            course.recommendedTime,
            course.tag,
            course.author.name,
            course.releaseTime,
            course.lessonCount,
            course_relation.finished
        ])
    return gen_standard_response(200, {'result': 'success',
                                       'message': f'my courses retrieved for {role} user {username}',
                                       'courses': course_list})


def assignable_task_list(request: HttpRequest):
    """
    获取一个用户可以分配给其他用户的全部任务
    """
    if request.method != 'GET':
        return illegal_request_type_error_response()
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if username is None or role is None:
        return session_timeout_response()
    task_list = []
    if role == 'admin':
        available_tasks = ContentTable.objects.filter(type=ContentTable.EnumType.Task)
    elif role == 'HRBP':
        task_templates = ContentTable.objects.filter(type=ContentTable.EnumType.Task,
                                                     isTemplate=True,
                                                     audience=1)
        authored_tasks = ContentTable.objects.filter(type=ContentTable.EnumType.Task,
                                                     isTemplate=False,
                                                     audience=1,
                                                     author__username=username)
        available_tasks = task_templates.union(authored_tasks)
    elif role == 'teacher':
        task_templates = ContentTable.objects.filter(type=ContentTable.EnumType.Task,
                                                     isTemplate=True,
                                                     audience=0)
        authored_tasks = ContentTable.objects.filter(type=ContentTable.EnumType.Task,
                                                     isTemplate=False,
                                                     audience=0,
                                                     author__username=username)
        available_tasks = task_templates.union(authored_tasks)
    else:  # newcomer
        return unauthorized_action_response()
    for task in available_tasks:
        if task.audience == 0:
            audience = 'newcomer'
        else:
            audience = 'teacher'
        if task.taskType == 0:
            task_type = 'text'
        elif task.taskType == 1:
            task_type = 'link'
        else:
            task_type = 'file'
        task_list.append([
            audience,
            task.isTemplate,
            task.name,
            task.intro,
            task.recommendedTime,
            task.tag,
            task.author.name,
            task.releaseTime,
            task_type,
            task.text,
            task.link
        ])
    return gen_standard_response(200, {'result': 'success',
                                       'message': f'assignable tasks retrieved for {role} user {username}',
                                       'tasks': task_list})


def my_task_list(request: HttpRequest):
    """
    获取一个用户可以完成的全部任务
    """
    if request.method != 'GET':
        return illegal_request_type_error_response()
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if username is None or role is None:
        return session_timeout_response()
    if role != 'teacher' and role != 'newcomer':
        return unauthorized_action_response()
    target_tasks = UserContentTable.objects.filter(user__username=username,
                                                   content__type=ContentTable.EnumType.Task)
    task_list = []
    for task_relation in target_tasks:
        task = task_relation.content
        if task.audience == 0:
            audience = 'newcomer'
        else:
            audience = 'teacher'
        if task.taskType == 0:
            task_type = 'text'
        elif task.taskType == 1:
            task_type = 'link'
        else:
            task_type = 'file'
        task_list.append([
            audience,
            task.isTemplate,
            task.name,
            task.intro,
            task.recommendedTime,
            task.tag,
            task.author.name,
            task.releaseTime,
            task_type,
            task.text,
            task.link,
            task_relation.finished
        ])
    return gen_standard_response(200, {'result': 'success',
                                       'message': f'my tasks retrieved for {role} user {username}',
                                       'tasks': task_list})


def teacher_newcomer_list(req: HttpRequest):
    """
    获得老师自己带的学生列表(已经毕业的不算)
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "GET",
        "username": "",
        "role": ["teacher"],
    })
    if not ok:
        return res
    teacher = PrivateInfo.objects.get(username=req.session.get("username"))
    student_list = TeacherNewcomerTable.objects.filter(teacher=teacher)
    learning_list = []
    for entry in student_list:  # 还在学习的学生
        if entry.newcomer.newcomerGraduateState == PrivateInfo.EnumNewcomerGraduateState.NotGraduate:
            learning_list.append(entry.newcomer)
    return_list = []
    for newcomer in learning_list:
        tmp = load_private_info(newcomer)
        tmp["graduated"] = GraduateStatusToTest[newcomer.newcomerGraduateState]  # temp
        tmp["evaluate"] = "暂无"
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(newcomer.username)  # 直接后端指定路径，前端自动请求
        return_list.append(tmp)

    return gen_response(200, data=return_list)
