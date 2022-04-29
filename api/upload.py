"""
所有上传新内容相关的接口
接口作者：@yzt @whh
"""
import os.path
import time
from re import split

import django.core.files.uploadedfile
import pandas as pd
from django.core.files import File
from django.core.files.base import ContentFile
from django.http import HttpRequest
from .api_util import *
from .models import *
import json

MAX_ALLOWED_COURSEWARES_FOR_ONE_LESSON = 10
EXAM_FILE_CACHE_MAX= 50
exam_file_cache = dict()


def create_program(request: HttpRequest):
    """
    创建一个Program
    """
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception:
        return gen_response(400, 'Load json request failed')
    user_session = request.session
    if user_session is None or "role" not in user_session.keys():  # session不存在
        return session_timeout_response()
    if user_session["role"] != "admin" and user_session["role"] != "teacher":  # 权限认证
        return unauthorized_action_response()
    # 从json中读取请求信息
    action = data.get("action")
    name = data.get("name")
    intro = data.get("intro")
    tag = data.get("tag")
    recommend_time = data.get("recommendTime")
    audience = data.get("audience")
    cover = data.get("cover")
    # 校验action字段、name字段和audience字段是否合规
    if action != "CreateProgram" or name is None or name == "" \
            or audience is None or (audience != "newcomer" and audience != "teacher"):
        return gen_standard_response(400, {"result": "failure", "message": "bad arguments"})
    if intro is None or intro == "":  # 无简介的话生成默认简介
        intro = "暂无简介"
    if audience == "teacher":  # API字段转换为数据库阶段
        audience_id = 1
    else:
        audience_id = 0
    if len(ProgramTable.objects.filter(name=name)) > 0:
        return gen_standard_response(200, {"result": "failure",
                                           "message": f"program {name} already exists",
                                           "programID": ProgramTable.objects.filter(name=name).first().id})
    username = user_session['username']
    new_program_id = username + "_p_" + str(time.time())  # 生成ProgramID 规则: username_p_time
    user = PrivateInfo.objects.filter(username=username).first() # 外键
    new_program = ProgramTable(id=new_program_id, name=name, author=user,
                               intro=intro, tag=tag, contentCount=0, recommendTime=recommend_time,
                               audience=audience_id, cover=cover)
    new_program.save()
    return gen_standard_response(200, {"result": "success",
                                       "message": f"program {name} created successfully",
                                       "programID": new_program_id})


def check_test_format(csv_file_path):
    with open(csv_file_path, "r", encoding="UTF-8") as csv_file:
        for row in csv_file.readlines():
            row = [item for item in row.split(',')]
            if len(row) < 3 or len(row) > 28:
                return False
            choice_cnt = len(row) - 2
            answers = [ans for ans in row[-1][:-1].split(' ')]
            print(answers)
            for answer in answers:
                if ord(answer) - ord('A') >= choice_cnt:
                    return False
    return True


def parse_test_for_student(csv_file_path):
    """
    返回不带答案的试卷
    """
    ret = []
    with open(csv_file_path, "r", encoding="UTF-8") as csv_file:
        for row in csv_file.readlines():
            row = [item for item in row[:-1].split(',')]
            ret.append(row[0: len(row) - 1])
    return ret


def parse_test_for_grader(csv_file_path):
    # TODO: 也需要改成和parse_test_for_admin一样的格式，等用到再改吧
    ret = []
    with open(csv_file_path, "r", encoding="UTF-8") as csv_file:
        for row in csv_file.readlines():
            row = [item for item in row[:-1].split(',')]
            ret.append(row[-1])
    return ret


def parse_test_for_admin(csv_file_path):
    ret = []
    with open(csv_file_path, "r", encoding="UTF-8") as csv_file:
        for row in csv_file.readlines():
            row = [item for item in row[:-1].split(',')]  # excel没一行
            
            choices = []  # 候选项
            for num in range(1, len(row) - 1):
                choices.append(row[num])
            
            answer_list = []  # 所有正确答案（因为可能是多选，所以需要存list）
            for answer in row[len(row) - 1].split(' '):
                answer_list.append(ord(answer) - ord('A'))  # 字母转数字：如字母'A'为0，'C'为2
            
            dict = {  # 每一个题目以一个字典格式传回
                'question': row[0],
                'choices': choices,
                'answer': answer_list, 
            }
            ret.append(dict)
            
    return ret


def upload_answers(request: HttpRequest):
    """
    判卷，格式：
    {action: "grade test", testID: __TEST_ID__, answer: ['A', 'BD', 'C', ...]}
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    # check arguments
    action = data.get('action')
    test_id = data.get('testID')
    answer_sheet = data.get('answer')
    if action != "grade test" or test_id is None or answer_sheet is None:
        return gen_standard_response(400, {"result": "failed", "message": "Bad Arguments"})
    # check login session
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if username is None or role is None:
        return session_timeout_response()
    if role != 'newcomer' and role != 'teacher':
        return unauthorized_action_response()
    # check database
    relation_filter = UserContentTable.objects.filter(content__id=test_id, user__username=username)
    test_filter = ContentTable.objects.filter(id=test_id)
    if len(relation_filter) == 0 or len(test_filter) == 0:
        return item_not_found_error_response()
    relation = relation_filter.first()
    test = test_filter.first()
    if test is None or test.type != ContentTable.EnumType.Exam:
        return item_not_found_error_response()
    # grade test paper
    valid, result = grade_test(answer_sheet, test)
    if not valid:
        return gen_standard_response(400, {"result": "failed", "message": "Answer sheet does not match exam"})
    # calculate score
    correct = 0
    for question in result:
        if question[2] is True:
            correct += 1
    score = correct / len(result) * 100
    # print(valid, result)
    relation.finished = True
    relation.userEndTime = datetime.datetime.now()
    relation.examUsedTime = int((relation.userEndTime - relation.userBeginTime).seconds)
    relation.score = score
    relation.save()
    # print(relation.finished, relation.userBeginTime, relation.userEndTime, relation.examUsedTime, relation.score)
    return gen_standard_response(200, {"result": "success",
                                       "message": "Test paper successfully graded",
                                       "results": [score, result]})


def begin_test(request: HttpRequest):
    """
    开始考试，记录开始时间
    {action: "start test", testID: __TEST_ID__}
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    # check arguments
    action = data.get('action')
    test_id = data.get('testID')
    if action != 'start test' or test_id is None:
        return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
    # check login session
    session = request.session
    username = session.get('username')
    print('username', username)
    role = session.get('role')
    if username is None or role is None:
        return session_timeout_response()
    if role != 'newcomer' and role != 'teacher':
        return unauthorized_action_response()
    # check database
    relation_filter = UserContentTable.objects.filter(content__id=test_id, user__username=username)
    test_filter = ContentTable.objects.filter(id=test_id)
    if len(relation_filter) == 0 or len(test_filter) == 0:
        return item_not_found_error_response()
    test = test_filter.first()
    relation = relation_filter.first()
    if test is None or test.type != ContentTable.EnumType.Exam:
        return item_not_found_error_response()
    # log begin time
    relation.userBeginTime = datetime.datetime.now()
    relation.save()
    # load test paper
    try:
        if test.questions == '' or test.questions is None:
            csv_dir = './files/test/SampleTestPaper.csv'
        else:
            csv_dir = test.questions
        fp = open(csv_dir, "r", encoding="UTF-8")
    except Exception as e:
        print(e)
        return item_not_found_error_response()
    test_paper = parse_test_for_student(csv_dir)
    return gen_standard_response(200, {"result": "success",
                                       "message": f"test for test {test.name} with id {test.id} started by {username}",
                                       "test": test_paper})


def grade_test(answer_sheet, test):
    """
    在线判卷，需要一个content_id
    """
    if test is None:
        return False, []
    if test.type != ContentTable.EnumType.Exam:
        return False, []
    if test.questions == '' or test.questions is None:
        csv_dir = './files/test/SampleTestPaper.csv'
    else:
        csv_dir = test.questions
    correct_answers = parse_test_for_grader(csv_dir)
    if len(answer_sheet) != len(correct_answers):
        return False, []
    res = []
    for i in range(len(answer_sheet)):
        # print(answer_sheet)
        answer_stu = answer_sheet[i]
        for j in range(len(answer_stu)):
            answer_stu[j] = chr(ord('A') + answer_stu[j])
        answer_std = correct_answers[i].split(" ")
        answer_stu.sort()
        answer_std.sort()
        print("student answer:", answer_stu, "standard answer:", answer_std)
        if len(answer_std) != len(answer_stu):
            res.append(False)
            continue
        correct = True
        for j in range(len(answer_stu)):
            if answer_stu[j] != answer_std[j]:
                correct = False
                break
        if correct:
            res.append([answer_sheet[i], correct_answers[i], True])
        else:
            res.append([answer_sheet[i], correct_answers[i], False])
    return True, res


def finish_task(request: HttpRequest):
    """
    结束任务
    {action: "finish task", taskID: __TASK_ID__}
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    # check arguments
    action = data.get('action')
    task_id = data.get('taskID')
    if action != 'finish task' or task_id is None:
        return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
    # check login session
    session = request.session
    username = session.get('username')
    print('username', username)
    role = session.get('role')
    if username is None or role is None:
        return session_timeout_response()
    if role != 'newcomer' and role != 'teacher':
        return unauthorized_action_response()
    # check database
    relation_filter = UserContentTable.objects.filter(user__username=username, content__id=task_id)
    task_filter = ContentTable.objects.filter(id=task_id)
    if len(relation_filter) == 0 or len(task_filter) == 0:
        return item_not_found_error_response()
    relation = relation_filter.first()
    task = task_filter.first()
    if task.type != ContentTable.EnumType.Task:
        return item_not_found_error_response()
    if relation.finished is True:
        return item_not_found_error_response()
    # log task finished
    relation.userEndTime = datetime.datetime.now()
    relation.finished = True
    relation.save()
    std_message = f'user {username} marked task {task.name} with id {task.id} as finished'
    return gen_standard_response(200, {'result': 'success',
                                       'message': std_message})


# def upload_test_file(request: HttpRequest):
#     '''
#     上传csv文件
#     '''
#     # 获取相对路径
#     print('enter upload_test_file')
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     if request.method == 'POST':
#         username = request.session.get('username')
#         role = request.session.get('role')
#         if username is None or role is None:
#             return session_timeout_response()
#         if role != "teacher" and role != "admin":
#             return unauthorized_action_response()
#         file = request.FILES.get('file', None)
#         # 设置文件上传文件夹
#         head_path = BASE_DIR + "/files/test"
#         print("head_path", head_path)
#         # 判断是否存在文件夹, 如果没有就创建文件路径
#         if not os.path.exists(head_path):
#             os.makedirs(head_path)
#         file_suffix = file.name.split(".")[1]  # 获取文件后缀
#         file_name = file.name.split(".")[0] + f"_{username}_ex_{time.time()}"  # 获取文件名字
#         # TODO: 后续应用testID替代目前的file_name!!!
#         # 储存路径
#         file_path = head_path + "/{}".format(file_name + "." + file_suffix)
#         file_path = file_path.replace(" ", "")
#         # 上传文件
#         with open(file_path, 'wb') as f:
#             for chunk in file.chunks():
#                 f.write(chunk)
#         check_test_format(file_path)
#         message = {}
#         message['code'] = 200
#         # 返回图片路径
#         message['fileurl'] = file_path
#         return JsonResponse(message)
#     else:
#         return illegal_request_type_error_response()


def save_test_file(file, username, test_id):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    head_path = base_dir + f"/files/test/{test_id}"
    print("head_path", head_path)
    # 判断是否存在文件夹, 如果没有就创建文件路径
    if not os.path.exists(head_path):
        os.makedirs(head_path)
    file_suffix = file.name.split(".")[1]  # 获取文件后缀
    file_name = file.name.split(".")[0] + f"_{username}_ex_{time.time()}"  # 获取文件名字
    # TODO: 后续应用testID替代目前的file_name!!!
    # 储存路径
    file_path = head_path + "/{}".format(file_name + "." + file_suffix)
    file_path = file_path.replace(" ", "")
    # 上传文件
    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    check_test_format(file_path)
    return file_path


def create_content(request: HttpRequest):
    """
    创建一个content(课程/考试/任务)
    """
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:
        # 读取信息
        action = request.POST.get('action')
        name = request.POST.get("name")
        intro = request.POST.get("intro")
        tag = request.POST.get("tag")
        recommend_time = request.POST.get("recommendTime")
        audience = request.POST.get("audience")
        cover = request.POST.get("cover")
        content_type = request.POST.get("type")
        is_template = str_to_boolean(request.POST.get("isTemplate"))
        csv = request.FILES.get("csv")
        program_id = request.POST.get("programID")
        task_type = request.POST.get("taskType")
        task_text = request.POST.get("taskText")
        task_link = request.POST.get("taskLink")
        task_file = request.POST.get("taskFile")
    except Exception:
        return gen_response(400, 'Load json request failed')
    # 这个巨大的if用于校验请求信息是否合规
    # 第1行 - action字段校验
    # 第2行 - name字段校验
    # 第3行 - audience字段校验
    # 第4行 - isTemplate字段校验
    # 第5行 - programID有效性校验
    print(name)
    print(content_type)
    print(audience)
    print(is_template)
    print(program_id)
    if action is None or (action != "CreateContentTemplate" and action != "create content")\
            or name is None or name == ""\
            or content_type is None or (content_type != "course" and content_type != "exam" and content_type != "task")\
            or audience is None or (audience != "teacher" and audience != "newcomer")\
            or is_template is None or (is_template is not True and is_template is not False)\
            or program_id is None or len(ProgramTable.objects.filter(id=program_id)) == 0:
        return gen_standard_response(400, {"result": "failure", "message": "bad arguments"})
    if content_type == "exam" and csv is None:  # exam类型的content必须有考题csv文件
        return gen_standard_response(400, {"result": "failure", "message": "exam paper not found"})
    if content_type == "task" and ((task_type == 0 and (task_text is None or task_text == ""))  # 文字型task必需有文字
                                   or (task_type == 1 and (task_link is None or task_link == ""))  # 链接型task必须有链接
                                   or (task_type == 2 and task_file is None)):  # 文件型task必须有文件
        return gen_standard_response(400, {"result": "failure", "message": "task content not found"})
    user_session = request.session
    if user_session is None or "role" not in user_session.keys() or "username" not in user_session.keys():  # session不存在
        return session_timeout_response()
    username = user_session['username']
    cur_role = user_session["role"]
    user = PrivateInfo.objects.filter(username=username).first()
    program = ProgramTable.objects.filter(id=program_id).first()
    if is_template == True and cur_role != "admin":
        return unauthorized_action_response()
    if is_template == False and cur_role != "admin" and cur_role != "teacher":
        return unauthorized_action_response()
    if intro is None or intro == "":
        intro = "暂无简介"
    new_content_id = username + "_c_" + str(time.time())  # 与program类似的ID生成机制
    if audience == "teacher":
        audience_id = 1
    else:
        audience_id = 0
    if is_template == "true":  # isTemplate字段转换
        is_template_bool = True
    else:
        is_template_bool = False
    if content_type == "course":  # type字段转换
        content_type_id = 0
    elif content_type == "exam":
        content_type_id = 1
    else:
        content_type_id = 2
    # if content_type == "exam":
    #     try:
    #         file = open(csv, 'r', encoding="UTF-8")
    #     except Exception as e:
    #         print(e)
    #         return item_not_found_error_response()
    test_file_url = save_test_file(csv, username, new_content_id)
    new_content = ContentTable(id=new_content_id, name=name, author=user,
                               intro=intro, tag=tag, recommendedTime=recommend_time,
                               audience=audience_id, cover=cover, type=content_type_id,
                               isTemplate=is_template, programId=program, lessonCount=0,
                               questions=test_file_url, taskType=task_type,
                               text=task_text, link=task_link, taskFile=File(task_file))
    new_content.save()
    print(new_content.questions)
    new_program_content_relation = ProgramContentTable(program=program, content=new_content)  # 和父program创建关联信息
    new_program_content_relation.save()
    program.contentCount += 1  # 父program的content数量累加
    program.save()
    return gen_standard_response(200, {
        "result": "success",
        "message": f"content {name} created successfully",
        "contentID": new_content_id
    })


def create_lesson(request: HttpRequest):
    """
    创建一个Lesson
    代码结构和create_content完全一致，就不重复注释了
    """
    if request.method != "POST":  # 只接受POST请求
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception:
        return gen_response(400, 'Load json request failed')
    action = data.get("action")
    name = data.get("name")
    intro = data.get("intro")
    recommend_time = data.get("recommendTime")
    cover = data.get("cover")
    is_template = data.get("isTemplate")
    content_id = data.get("contentID")
    if action is None or (action != "CreateLessonTemplate" and action != "create lesson")\
            or name is None or name == ""\
            or is_template is None or (is_template is not True and is_template is not False)\
            or content_id is None or len(ContentTable.objects.filter(id=content_id)) == 0:
        return gen_standard_response(400, {"result": "failure", "message": "bad arguments"})
    user_session = request.session
    if user_session is None or "role" not in user_session.keys() or "username" not in user_session.keys():  # session不存在
        return session_timeout_response()
    username = user_session['username']
    cur_role = user_session["role"]
    user = PrivateInfo.objects.filter(username=username).first()
    content = ContentTable.objects.filter(id=content_id).first()
    if is_template == True and cur_role != "admin":
        return unauthorized_action_response()
    if is_template == False and cur_role != "admin" and cur_role != "teacher":
        return unauthorized_action_response()
    if intro is None or intro == "":
        intro = "暂无简介"
    new_lesson_id = username + "_l_" + str(time.time())
    new_lesson = LessonTable(id=new_lesson_id, name=name, author=user, content=content,
                             intro=intro, recommendedTime=recommend_time, cover=cover)
    new_lesson.save()
    content.lessonCount += 1
    content.save()
    return gen_standard_response(200, {
        "result": "success",
        "message": f"lesson {name} created successfully",
        "contentID": new_lesson_id
    })


# def save_courseware_file(lesson_id, order, creator_username, dir_prefix, file):
#     file_ext = file.name.split(".")[-1].lower()
#     file_path = f"{dir_prefix}/{lesson_id}/"
#     file_dir = f"{dir_prefix}/{lesson_id}/{order}_{file.name}"
#     try:
#         if not os.path.exists(file_path):
#             os.makedirs(file_path)
#         with open(file_dir, "wb+") as dest:
#             for chunk in file.chunks():
#                 dest.write(chunk)
#     except Exception:
#         return False, file_dir
#     return True, file_dir


# def upload_courseware_info(request: HttpRequest):
#     if request.method != "POST":  # 只接受POST请求
#         return illegal_request_type_error_response()
#     try:
#         data = json.loads(request.body)
#     except Exception:
#         return gen_response(400, 'Load json request failed')
#     order = data.get('order')
#     lesson_id = data.get('lessonID')
#     cover = data.get('cover')
#     if order not in range(1, MAX_ALLOWED_COURSEWARES_FOR_ONE_LESSON):
#         return gen_standard_response(400, {"result": "failed", "message": "too many coursewares"})
#     if len(LessonTable.objects.filter(id=lesson_id)) == 0:
#         return gen_standard_response(400, {"result": "failed", "message": "lesson not found"})
#     user_session = request.session
#     if user_session is None or "role" not in user_session.keys() or "user" not in user_session.keys():  # session不存在
#         return session_timeout_response()
#     username = user_session["username"]
#     cur_role = user_session["role"]
#     if cur_role != "admin" or cur_role != "teacher":  # 身份不是管理员或者导师
#         return unauthorized_action_response()
#     user_session["upload_lesson_id"] = lesson_id
#     user_session["upload_courseware_order"] = order
#     user_session["upload_cover"] = cover
#     std_success_message = f"info of courseware for lesson {lesson_id} registered"
#     return gen_standard_response(200, {"result": "success", "message": std_success_message})
#
#
# def upload_courseware_file(request: HttpRequest):
#     if request.method != "POST":  # 只接受POST请求
#         return illegal_request_type_error_response()
#     user_session = request.session
#     if user_session is None or "role" not in user_session.keys() or "user" not in user_session.keys():  # session不存在
#         return session_timeout_response()
#     username = user_session["username"]
#     cur_role = user_session["role"]
#     lesson_id = user_session.get("upload_lesson_id")
#     order = user_session.get("upload_courseware_order")
#     cover = user_session.get("upload_cover")
#     if lesson_id is None or order is None or cover is None:  # 调用upload_courseware_info接口时没有存参数
#         return gen_standard_response(400, {"result": "failure", "message": "bad arguments"})
#     # 删除相关参数，防止被复用
#     user_session.delete("upload_lesson_id")
#     user_session.delete("upload_courseware_order")
#     user_session.delete("upload_cover")
#     if cur_role != "admin" or cur_role != "teacher":  # 身份不是管理员或者导师
#         return unauthorized_action_response()
#     file_op_ret = save_courseware_file(lesson_id, order, username, 'files/lesson',
#                                        request.FILES.get("file"))
#     if file_op_ret[0]:
#         new_courseware_id = username + "_cw_" + str(time.time())
#         lesson = LessonTable.objects.filter(id=lesson_id).first()
#         content = lesson.content
#         new_courseware = CoursewareTable(id=new_courseware_id, lesson=lesson_id, content=content,
#                                          name=request.FILES.get("content").name, cover=cover, url=file_op_ret[1])
#         new_courseware.save()
#         std_success_message = f"courseware for lesson {lesson_id} uploaded successfully"
#         return gen_standard_response(200, {"result": "success", "message": std_success_message})
#     else:
#         std_error_message = "file system failed to save uploaded file. better luck next time:("
#         return gen_standard_response(400, {"result": "success", "message": std_error_message})


# def save_test_file(program_id, creator_username, dir_prefix, file):
#     file_ext = file.name.split(".")[-1].lower()
#     file_path = f"{dir_prefix}/{program_id}/"
#     file_dir = f"{dir_prefix}/{program_id}/{file.name}"
#     try:
#         if not os.path.exists(file_path):
#             os.makedirs(file_path)
#         with open(file_dir, "wb+") as dest:
#             for chunk in file.chunks():
#                 dest.write(chunk)
#     except Exception:
#         return False, file_dir
#     return True, file_dir
#
#
# def upload_test_file(request: HttpRequest):
#     if request.method != "POST":  # 只接受POST请求
#         return illegal_request_type_error_response()
#     user_session = request.session
#     if user_session is None or "role" not in user_session.keys() or "user" not in user_session.keys():  # session不存在
#         return session_timeout_response()
#     username = user_session["username"]
#     cur_role = user_session["role"]
#     program_id = user_session.get("upload_program_id")
#     cover = user_session.get("upload_cover")
#     # 删除相关参数，防止被复用
#     user_session.delete("upload_program_id")
#     user_session.delete("upload_cover")
#     if cur_role != "admin" or cur_role != "teacher":  # 身份不是管理员或者导师
#         return unauthorized_action_response()
#     file_op_ret = save_test_file(program_id, username, 'files/test',
#                                            request.FILES.get("content"))
#     if file_op_ret[0]:
#         new_test_id = username + "_t_" + str(time.time())
#         program = ProgramTable.objects.filter(id=program_id).first()
#         content = lesson.content
#         new_courseware = CoursewareTable(id=new_courseware_id, lesson=lesson_id, content=content,
#                                          name=request.FILES.get("content").name, cover=cover, url=file_op_ret[1])
#         new_courseware.save()
#         std_success_message = f"courseware for lesson {lesson_id} uploaded successfully"
#         return gen_standard_response(200, {"result": "success", "message": std_success_message})
#     else:
#         std_error_message = "file system failed to save uploaded file. better luck next time:("
#         return gen_standard_response(400, {"result": "success", "message": std_error_message})


def upload_lesson_file(request):
    '''
    上传pptx文件
    '''
    # 获取相对路径
    print('enter upload_lesson_file')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        # 设置文件上传文件夹
        head_path = BASE_DIR + "/files/lesson"
        print("head_path", head_path)
        # 判断是否存在文件夹, 如果没有就创建文件路径
        if not os.path.exists(head_path):
            os.makedirs(head_path)
        file_suffix = file.name.split(".")[1]  # 获取文件后缀
        file_name = file.name.split(".")[0]  # 获取文件名字
        # TODO: 后续应用classID_lessonID替代目前的file_name!!!
        # 储存路径
        file_path = head_path + "/{}".format(file_name + "." + file_suffix)
        file_path = file_path.replace(" ", "")
        # 上传文件
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        message = {}
        message['code'] = 200
        # 返回图片路径
        message['fileurl'] = file_path

        return JsonResponse(message)

