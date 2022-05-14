import json

from .api_util import *
from .models import *
from .upload import parse_test_for_student, parse_test_for_admin

audience_select = ["newcomer", "teacher"]
task_type_select = ["text", "link", "file"]


def admin_newcomer_list(request: HttpRequest):
    """
    接收前端向/admin_newcomer_list的get请求
    获取所有新人的数据
    仅限管理员使用
    TODO
    """
    ok, res = quick_check(request, {
        "method": "GET",
        "username": "",
        "role": ["admin"],
    })
    if not ok:
        return res
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
        state_select = [False, True, True]
        tmp["graduated"] = state_select[newcomer.newcomerGraduateState]
        tmp["evaluate"] = "暂无"
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(newcomer.username)  # 直接后端指定路径，前端自动请求
        return_list.append(tmp)
    return gen_response(200, return_list, "tmp supported")


def admin_all_user_list(request: HttpRequest):
    ok, res = quick_check(request, {
        "method": "GET",
        "username": "",
        "role": ["admin"],
    })
    if not ok:
        return res
    user_list = PrivateInfo.objects.all()
    return_list = []
    for user in user_list:
        tmp = load_private_info(user)
        tmp["joinBootcamp"] = True
        state_select = [False, True, True]
        tmp["graduated"] = state_select[user.newcomerGraduateState]
        tmp["evaluate"] = "暂无"
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(user.username)  # 直接后端指定路径，前端自动请求
        return_list.append(tmp)
    return gen_response(200, return_list, "tmp supported")


def teacher_wait_list(req: HttpRequest):
    """
    权限确认(admin)
    筛选出导师候选人(已经完成新人培训的新人),返回基本信息列表
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "GET",
        "username": "",
        "role": ["admin"],
    })
    if not ok:
        return res
    newcomer_list = PrivateInfo.objects.filter(
        isTeacher=False, isNew=True, newcomerGraduateState=PrivateInfo.EnumNewcomerGraduateState.NormalGraduate)
    return_list = []
    for new in newcomer_list:
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
    ok, res = quick_check(req, {
        "method": "GET",
        "username": "",
        "role": ["admin"],
    })
    if not ok:
        return res
    teacher_list = PrivateInfo.objects.filter(isTeacher=True, teacherIsDuty=False)
    return_list = []
    for teacher in teacher_list:
        tmp = load_private_info(teacher)
        tmp["teacherNominationDate"] = teacher.teacherNominationDate
        status = teacher.teacherExaminedStatus
        tmp["teacherExaminedStatus"] = TeacherExaminedStatusToTest[status]
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
    """
    获取正在上岗的导师列表
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "GET",
        "username": "",
        "role": ["admin", "HRBP"],
    })
    if not ok:
        return res
    teacher_list = PrivateInfo.objects.filter(isTeacher=True, teacherIsDuty=True)
    return_list = []
    for teacher in teacher_list:
        tmp = load_private_info(teacher)
        # 计算teacher score
        relations = TeacherNewcomerTable.objects.filter(teacher=teacher)
        total_scores = sum([relation.teacherScore for relation in relations])
        if len(relations) <= 0:
            teacher.teacherScore = 0
        else:
            teacher.teacherScore = total_scores/len(relations)
        teacher.save()
        tmp["historicalMembers"] = teacher.historicalMembers
        tmp["currentMembers"] = teacher.currentMembers
        tmp["totalMembers"] = teacher.currentMembers + teacher.historicalMembers
        tmp["teacherDutyDate"] = teacher.teacherDutyDate
        tmp["teacherScore"] = teacher.teacherScore
        tmp["OKR"] = "unknown"
        tmp["avatar"] = "/api/avatar_by_name/?username={}".format(teacher.username)
        return_list.append(tmp)
    return gen_response(200, data=return_list, message="send {} data".format(len(return_list)))


def nominated_list(req: HttpRequest):
    """
    已经被提名,可以进行审核的教师列表
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
    teacher_list = PrivateInfo.objects.filter(
        isTeacher=True, teacherIsDuty=False,
        teacherExaminedStatus=PrivateInfo.EnumTeacherExaminedStatus.NotYet)
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
            audience = audience_select[test.audience]
            test_info = {
                'audience': audience,
                'isTemplate': test.isTemplate,
                'name': test.name,
                'intro': test.intro,
                'recommendTime': str(test.recommendedTime),
                'tag': str2taglist(test.tag),
                'author': test.author.name,
                'releaseTime': test.releaseTime,
                'contentID': test.id,
                'isObligatory': test.isObligatory,
            }
            recommend_time_list.append(str(test.recommendedTime))
            tag_list.extend(str2taglist(test.tag))
            try:
                # if test.questions == '' or test.questions is None:
                #     csv_dir = './files/test/SampleTestPaper.csv'
                # else:
                #     csv_dir = test.questions
                csv_dir = test.questions
                fp = open(csv_dir, "r", encoding="UTF-8")
                fp.close()
            except Exception as e:
                print(e)
                return item_not_found_error_response()
            print(csv_dir)
            test_paper = parse_test_for_admin(csv_dir)
            test_list.append(test_info)
        print(test_list)
        recommend_time_list = list(set(recommend_time_list))
        tag_list = list(set(tag_list))
        return gen_standard_response(200, {'result': 'success',
                                           'message': f'assignable tests retrieved for admin user {username}',
                                           'tests': test_list, 'test_recommend_time_items': recommend_time_list,
                                           'test_tag_items': tag_list})
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
        recommend_time_list = []
        tag_list = []
        for test in available_tests:
            audience = audience_select[test.audience]
            test_info = {
                'audience': audience,
                'isTemplate': test.isTemplate,
                'name': test.name,
                'intro': test.intro,
                'recommendTime': str(test.recommendedTime),
                'tag': str2taglist(test.tag),
                'author': test.author.name,
                'releaseTime': test.releaseTime,
                'contentID': test.id,
                'isObligatory': test.isObligatory,
            }
            recommend_time_list.append(str(test.recommendedTime))
            tag_list.extend(str2taglist(test.tag))
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
            test_list.append(test_info)
        print(test_list)
        recommend_time_list = list(set(recommend_time_list))
        tag_list = list(set(tag_list))
        return gen_standard_response(200, {'result': 'success',
                                           'message': f'assignable tests retrieved for teacher user {username}',
                                           'tests': test_list, 'test_recommend_time_items': recommend_time_list,
                                           'test_tag_items': tag_list})
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
        recommend_time_list = []
        tag_list = []
        for test in available_tests:
            audience = audience_select[test.audience]
            test_info = {
                'audience': audience,
                'isTemplate': test.isTemplate,
                'name': test.name,
                'intro': test.intro,
                'recommendTime': str(test.recommendedTime),
                'tag': str2taglist(test.tag),
                'author': test.author.name,
                'releaseTime': test.releaseTime,
                'contentID': test.id,
                'isObligatory': test.isObligatory,
            }
            recommend_time_list.append(str(test.recommendedTime))
            tag_list.extend(str2taglist(test.tag))
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
            test_list.append(test_info)
        print(test_list)
        recommend_time_list = list(set(recommend_time_list))
        tag_list = list(set(tag_list))
        return gen_standard_response(200, {'result': 'success',
                                           'message': f'assignable tests retrieved for hrbp user {username}',
                                           'tests': test_list, 'test_recommend_time_items': recommend_time_list,
                                           'test_tag_items': tag_list})
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
    if role == "teacher":
        audience = ContentTable.EnumAudience.teacher
    else:
        audience = ContentTable.EnumAudience.newcomer
    target_tests = UserContentTable.objects.filter(
        user__username=username, content__type=ContentTable.EnumType.Exam,
        content__audience=audience
    )
    test_list = []
    # recommend_time_list = []
    # tag_list = []
    for test_relation in target_tests:
        test = test_relation.content
        audience = audience_select[test.audience]
        test_info = {
            'audience': audience,
            'isTemplate': test.isTemplate,
            'name': test.name,
            'intro': test.intro,
            'recommendTime': str(test.recommendedTime),
            'tag': str2taglist(test.tag),
            'isObligatory': test.isObligatory,
            'author': test.author.name,
            'releaseTime': test.releaseTime,
            'contentID': test.id,
            'isFinished': test_relation.finished,
            'score': test_relation.score,
            'examUsedTime': test_relation.examUsedTime,
        }
        # recommend_time_list.append(str(test.recommendedTime))
        # tag_list.append(test.tag)
        """try:
            # if test.questions == '' or test.questions is None:
            #     csv_dir = './files/test/SampleTestPaper.csv'
            # else:
            #     csv_dir = test.questions
            csv_dir = test.questions
            fp = open(csv_dir, "r", encoding="UTF-8")
        except Exception as e:
            print(e)
            return item_not_found_error_response()
        test_paper = parse_test_for_student(csv_dir)"""  # 用来返回考试内容（考题）
        # test_list.append({'test_info': test_info, 'test_paper': test_paper})
        test_list.append(test_info)
    print(test_list)
    # recommend_time_list = list(set(recommend_time_list))
    # tag_list = list(set(tag_list))
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
        audience = audience_select[course.audience]
        course_list.append({
            'audience': audience,
            'isTemplate': course.isTemplate,
            'name': course.name,
            'intro': course.intro,
            'recommendTime': course.recommendedTime,
            'tag': str2taglist(course.tag),
            'isObligatory': course.isObligatory,
            'author': course.author.name,
            'releaseTime': course.releaseTime,
            'lessonCount': course.lessonCount,
            'programID': course.programId.id,
            'contentID': course.id
        })
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
    if role == "teacher":
        audience = ContentTable.EnumAudience.teacher
    else:
        audience = ContentTable.EnumAudience.newcomer
    target_courses = UserContentTable.objects.filter(
        user__username=username,
        content__type=ContentTable.EnumType.Course,
        content__audience=audience
    )
    course_list = []
    for course_relation in target_courses:
        course = course_relation.content
        audience = audience_select[course.audience]
        course_list.append({
            'audience': audience,
            'isTemplate': course.isTemplate,
            'name': course.name,
            'intro': course.intro,
            'recommendTime': course.recommendedTime,
            'tag': str2taglist(course.tag),
            'isObligatory': course.isObligatory,
            'author': course.author.name,
            'releaseTime': course.releaseTime,
            'lessonCount': course.lessonCount,
            'isFinished': course_relation.finished,
            'finishedLessonCount': course_relation.finishedLessonCount,
            # 'programID': course.programId,
            'contentID': course.id
        })
    print(course_list)
    return gen_standard_response(200, {'result': 'success',
                                       'message': f'my courses retrieved for {role} user {username}',
                                       'courses': course_list})


# def my_course_list_by_id(request: HttpRequest):
#     """
#     {'action': 'course list by username', 'username': '__USERNAME__'}
#     """
#     ok, res = quick_check(request, {
#         "method": "POST",
#         "data_field": []
#     })
#     if not ok:
#         return res
#     data = json.loads(request.body)
#     action = data.get('action')
#     target_username = data.get('username')
#     if action != 'course list by id' or target_username is None:
#         return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
#     session = request.session
#     username = session.get('username')
#     role = session.get('role')
#     if username is None or role is None:
#         return session_timeout_response()
#     if role != 'admin' and role != 'teacher' and role != 'HRBP':
#         return unauthorized_action_response()
#     user = PrivateInfo.objects.filter(username=target_username).first()
#     if user is None:
#         return item_not_found_error_response()
#     relations = UserContentTable.objects.filter(user__username=target_username, content__type=0)
#     course_list = []
#     for relation in relations:
#         course = relation.content
#         if course.audience == 0:
#             audience = 'newcomer'
#         else:
#             audience = 'teacher'
#         course_list.append({
#             'courseID': course.id,
#             'audience': audience,
#             'isTemplate': course.isTemplate,
#             'name': course.name,
#             'intro': course.intro,
#             'recommendTime': course.recommendedTime,
#             'tag': course.tag,
#             'author': course.author.name,
#             'releaseTime': course.releaseTime,
#             'lessonCount': course.lessonCount,
#             'finished': relation.finished
#         })
#     return gen_standard_response(200, {'result': 'success',
#                                        'message': f'courses retrieved for user {target_username} by {username}',
#                                        'courses': course_list})


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
    recommend_time_list = []
    tag_list = []
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
        audience = audience_select[task.audience]
        task_type = task_type_select[task.taskType]
        task_list.append({
            'audience': audience,
            'isTemplate': task.isTemplate,
            'name': task.name,
            'intro': task.intro,
            'recommendTime': str(task.recommendedTime),
            'tag': str2taglist(task.tag),
            'isObligatory': task.isObligatory,
            'author': task.author.name,
            'releaseTime': task.releaseTime,
            'taskType': task_type,
            'taskText': task.text,
            'taskLink': task.link,
            'contentID': task.id
        })
        recommend_time_list.append(str(task.recommendedTime))
        tag_list.extend(str2taglist(task.tag))
    recommend_time_list = list(set(recommend_time_list))
    tag_list = list(set(tag_list))
    return gen_standard_response(200, {'result': 'success',
                                       'message': f'assignable tasks retrieved for {role} user {username}',
                                       'tasks': task_list, 'task_recommend_time_items': recommend_time_list,
                                       'task_tag_items': tag_list})


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
    if role == "teacher":
        audience = ContentTable.EnumAudience.teacher
    else:
        audience = ContentTable.EnumAudience.newcomer
    target_tasks = UserContentTable.objects.filter(
        user__username=username,
        content__type=ContentTable.EnumType.Task,
        content__audience=audience
    )
    task_list = []
    recommend_time_list = []
    tag_list = []
    for task_relation in target_tasks:
        task = task_relation.content
        audience = audience_select[task.audience]
        task_type = task_type_select[task.taskType]
        task_list.append({
            'audience': audience,
            'isTemplate': task.isTemplate,
            'name': task.name,
            'intro': task.intro,
            'recommendTime': str(task.recommendedTime),
            'tag': str2taglist(task.tag),
            'isObligatory': task.isObligatory,
            'author': task.author.name,
            'releaseTime': task.releaseTime,
            'taskType': task_type,
            'taskText': task.text,
            'taskLink': task.link,
            'isFinished': task_relation.finished,
            'contentID': task.id
        })
        recommend_time_list.append(str(task.recommendedTime))
        tag_list.extend(str2taglist(task.tag))
    recommend_time_list = list(set(recommend_time_list))
    tag_list = list(set(tag_list))
    return gen_standard_response(200, {'result': 'success',
                                       'message': f'my tasks retrieved for {role} user {username}',
                                       'tasks': task_list, 'task_recommend_time_items': recommend_time_list,
                                       'task_tag_items': tag_list})


def program_template_list(request: HttpRequest):
    """
    获取模板项目列表
    :param request:
    :return:
    """
    ok, res = quick_check(request, {
        "method": "GET",
        "username": "",  # 检查session
        "cur_role": [],  # 检查session
    })
    if not ok:
        return res
    session = request.session
    role = session.get('role')
    if role != 'teacher' and role != 'admin' and role != 'HRBP':
        return unauthorized_action_response()
    target_programs = []
    program_templates = ProgramTable.objects.filter(isTemplate=True)
    for program in program_templates:
        audience = audience_select[program.audience]
        program_info = dict()
        program_info['name'] = program.name
        program_info['author'] = program.author.username
        program_info['intro'] = program.intro
        program_info['contentCount'] = program.contentCount
        program_info['recommendTime'] = program.recommendTime
        program_info['audience'] = audience
        # program_info['cover'] = program.cover
        program_info['releaseTime'] = program.releaseTime
        program_info['isTemplate'] = program.isTemplate
        program_info['programID'] = program.id
        target_programs.append(program_info)
    return gen_standard_response(200, {'result': 'success',
                                       'message': 'all program templates retrieved',
                                       'program_templates': target_programs})


def assignable_program_list(request: HttpRequest):
    """
    获取可分配的项目
    :param request:
    :return:
    """
    ok, res = quick_check(request, {
        "method": "GET",
        "username": "",  # 检查session
        "cur_role": [],  # 检查session
    })
    if not ok:
        return res
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if role != 'admin' and role != 'teacher' and role != 'HRBP':
        return unauthorized_action_response()

    program_templates = ProgramTable.objects.filter(isTemplate=True)
    authored_programs = ProgramTable.objects.filter(isTemplate=False,
                                                    author__username=username)
    available_programs = program_templates.union(authored_programs)
    target_programs = []
    for program in available_programs:
        if UserProgramTable.objects.filter(program=program).count() != 0:
            continue
        audience = audience_select[program.audience]
        program_info = dict()
        program_info['name'] = program.name
        program_info['author'] = program.author.username
        program_info['intro'] = program.intro
        program_info['contentCount'] = program.contentCount
        program_info['recommendTime'] = program.recommendTime
        program_info['audience'] = audience
        # program_info['cover'] = program.cover
        program_info['releaseTime'] = program.releaseTime
        program_info['isTemplate'] = program.isTemplate
        program_info['programID'] = program.id
        target_programs.append(program_info)
    return gen_standard_response(200, {'result': 'success',
                                       'message': 'all assignable programs retrieved',
                                       'program_templates': target_programs})


# def my_program_list(request: HttpRequest):
#     """
#     获取自己的program
#     :param request:
#     :return:
#     """
#     if request.method != 'GET':
#         return illegal_request_type_error_response()
#     session = request.session
#     username = session.get('username')
#     role = session.get('role')
#     if username is None or role is None:
#         return session_timeout_response()
#     if role != 'teacher' and role != 'newcomer':
#         return unauthorized_action_response()
#     my_relations = UserProgramTable.objects.filter(user__username=username)
#     target_programs = []
#     for relation in my_relations:
#         program = relation.program
#         audience = audience_select[program.audience]
#         program_info = dict()
#         program_info['name'] = program.name
#         program_info['author'] = program.author.username
#         program_info['intro'] = program.intro
#         program_info['contentCount'] = program.contentCount
#         program_info['recommendTime'] = program.recommendTime
#         program_info['audience'] = audience
#         # program_info['cover'] = program.cover
#         program_info['releaseTime'] = program.releaseTime
#         program_info['isTemplate'] = program.isTemplate
#         program_info['programID'] = program.id
#         target_programs.append(program_info)
#     return gen_standard_response(200, {'result': 'success',
#                                        'message': 'my programs retrieved',
#                                        'program_templates': target_programs})


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


def program_content_list(request: HttpRequest):
    """
    POST{
    'action': 'get content list for program'
    'programID': '__PROGRAM_ID__'
    }
    """
    ok, res = quick_check(request, {
        "method": "POST",
        "username": "",
        "cur_role": [],  # 如果列表为空，则只检查session中是否存在role
        "data_field": []
    })
    if not ok:
        return res
    data = json.loads(request.body)
    action = data.get('action')
    program_id = data.get('programID')
    if action != 'get content list for program' or program_id is None:
        return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
    program = ProgramTable.objects.filter(id=program_id).first()
    if program is None:
        return item_not_found_error_response()
    relations = ProgramContentTable.objects.filter(program__id=program_id)
    courses = []
    tests = []
    tasks = []
    user_program_relation = UserProgramTable.objects.filter(program__id=program_id).first()
    if user_program_relation is not None:
        target_user = user_program_relation.user
    type_select = ["course", "exam", "task"]
    for relation in relations:
        content = relation.content
        audience = audience_select[content.audience]
        content_type = type_select[content.type]
        task_type = task_type_select[content.taskType]
        content_info = {
            'name': content.name,
            'author': content.author.username,
            'intro': content.intro,
            'tag': str2taglist(content.tag),
            'isObligatory': content.isObligatory,
            'recommendTime': content.recommendedTime,
            'audience': audience,
            'contentType': content_type,
            'isTemplate': content.isTemplate,
            'programID': program_id,
            'releaseTime': content.releaseTime,
            'lessonCount': content.lessonCount,
            'beginTime': content.beginTime,
            'endTime': content.endTime,
            'taskType': task_type,
            'taskText': content.text,
            'taskLink': content.link,
            'contentID': content.id
        }
        if user_program_relation is not None:
            user_content_relation = UserContentTable.objects.filter(user=target_user, content=content).first()
            content_info['isFinished'] = user_content_relation.finished
            content_info['finishedLessonCount'] = user_content_relation.finishedLessonCount
            content_info['score'] = user_content_relation.score
            content_info['examUsedTime'] = user_content_relation.examUsedTime
        if content.type == 0:
            courses.append(content_info)
        elif content.type == 1:
            tests.append(content_info)
        else:
            tasks.append(content_info)
    total_len = len(courses) + len(tests) + len(tasks)
    return gen_standard_response(200, {'result': 'success',
                                       'message': f'{total_len} contents retrieved for program {program_id}',
                                       'courses': courses,
                                       'tests': tests,
                                       'tasks': tasks})


def teacher_newcomer_list_by_name(req: HttpRequest):
    """
    管理员通过姓名来获取导师的学生列表
    :param req:
    :return:
    """
    ok, res = quick_check(req, {
        "method": "POST",
        "username": "",
        "role": ["admin"],
        "data_field": ["teacher"]
    })
    if not ok:
        return res
    data = json.loads(req.body)
    found, teacher = find_people(data["teacher"])
    if not found:
        return teacher
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
    return gen_response(200, return_list)


def content_lesson_list(request: HttpRequest):
    """
    获取content的lesson列表
    POST
    {
        'action': 'lesson list for course'
        'contentID': __CONTENT_ID__
    }
    """
    ok, res = quick_check(request, {
        "method": "POST",
        "data_field": [],
        "username": "",  # 检查session
        "cur_role": [],  # 检查session
    })
    if not ok:
        return res
    data = json.loads(request.body)
    action = data.get('action')
    content_id = data.get('contentID')
    if action != 'lesson list for course' or content_id is None:
        return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
    course = ContentTable.objects.filter(id=content_id).first()
    if course is None:
        return item_not_found_error_response()
    lessons = LessonTable.objects.filter(content__id=content_id)
    lesson_list = []
    for lesson in lessons:
        lesson_list.append({
            'lessonID': lesson.id,
            'name': lesson.name,
            'author': lesson.author.username,
            'intro': lesson.intro,
            'recommendTime': lesson.recommendedTime,
            'releaseTime': lesson.releaseTime
        })
    logging.info(lesson_list)
    return gen_standard_response(200, {
        'result': 'success',
        'message': f'{len(lessons)} lessons retrieved for course {course.name}',
        'lessons': lesson_list
    })


def lesson_courseware_list(request: HttpRequest):
    """
    POST
    {
        'action': 'courseware list for lesson'
        'lessonID': __LESSON_ID__
    }
    """
    ok, res = quick_check(request, {
        "method": "POST",
        "data_field": [],
        "username": "",  # 检查session
        "cur_role": [],  # 检查session
    })
    if not ok:
        return res
    data = json.loads(request.body)
    action = data.get('action')
    lesson_id = data.get('lessonID')
    if action != 'courseware list for lesson' or lesson_id is None:
        return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
    lesson = LessonTable.objects.filter(id=lesson_id).first()
    if lesson is None:
        return item_not_found_error_response()
    coursewares = CoursewareTable.objects.filter(lesson__id=lesson_id)
    courseware_list = []
    for courseware in coursewares:
        courseware_list.append({
            'coursewareID': courseware.id,
            'name': courseware.name,
            'uploadTime': courseware.uploadTime,
            'url': courseware.url
        })
    return gen_standard_response(200, {
        'result': 'success',
        'message': f'{len(coursewares)} coursewares retrieved for lesson {lesson.name}',
        'lessons': courseware_list
    })
