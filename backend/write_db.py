"""
提供api进行数据库的写入
"""
from django.http import HttpRequest
from api.models import *
from utils.reader import get_root_path, open_xlsx, encrypt
import pandas as pd
import logging
from api.api_util import gen_response


def write_db(req: HttpRequest):
    if req.method == "POST":
        path = "/testcase/template.xlsx"
    else:
        path = "/testcase/real.xlsx"
    root = get_root_path()
    df: pd.DataFrame = open_xlsx(str(root) + path, "privateinfo")
    for i in range(len(df)):
        info = df.iloc[i]
        if len(PrivateInfo.objects.filter(username=info["username"])) > 0:
            continue
        pv = PrivateInfo(
            password=encrypt(info["password"]),
            username=info["username"],

            name=info["name"],
            city=info["city"],
            dept=info["dept"],
            bio=info["bio"],
            joinDate=info["joinDate"],
            joinStatus=info["joinStatus"],
            detail=info["detail"],
            leader=info["leader"],
            registrationDate=str(info["registrationDate"]),
            employeeType=info["employeeType"],
            avatar=str(root) + "/static/头像.jpeg",

            isAdmin=info["isAdmin"],
            isTeacher=info["isTeacher"],
            isHRBP=info["isHRBP"],
            isNew=info["isNew"],

            newcomerStartDate=str(info["newcomerStartDate"]),
            newcomerGraduateState=info["newcomerGraduateState"],
            newcomerGraduateDate=str(info["newcomerGraduateDate"]),

            historicalMembers=info["historicalMembers"],
            currentMembers=info["currentMembers"],
            teacherNominationDate=info["teacherNominationDate"],
            teacherExaminedStatus=info["teacherExaminedStatus"],
            teacherExaminedDate=info["teacherExaminedDate"],
            teacherIsDuty=info["teacherIsDuty"],
            teacherDutyDate=str(info["teacherDutyDate"]),
            teacherScore=info["teacherScore"],
        )
        pv.save()
    size = len(PrivateInfo.objects.all())
    # logging.info("{} private info loaded".format(size))

    df: pd.DataFrame = open_xlsx(str(root) + path, "honor")
    for i in range(len(df)):
        info = df.iloc[i]
        owner = PrivateInfo.objects.get(username=info["owner"])
        honor = Honor(
            text=info["text"],
            type=info["type"],
            owner=owner
        )
        honor.save()
    size = len(Honor.objects.all())
    # logging.info("{} honor inf loaded".format(size))

    df: pd.DataFrame = open_xlsx(str(root) + path, "teachernewcomertable")
    for i in range(len(df)):
        info = df.iloc[i]
        teacher = PrivateInfo.objects.get(username=info["teacher"])
        newcomer = PrivateInfo.objects.get(username=info["newcomer"])
        tnt = TeacherNewcomerTable(
            newcomer=newcomer,
            teacher=teacher,
            teacherScore=info["teacherScore"],
            newcomerToTeacher=info["newcomerToTeacher"],
            newcomerScore=info["newcomerScore"],
            teacherToNewcomer=info["teacherToNewcomer"],
            teacherCommitted=info["teacherCommitted"],
            newcomerCommitted=info["newcomerCommitted"]
        )
        tnt.save()
    size = len(TeacherNewcomerTable.objects.all())
    # logging.info("{} teacher newcomer info loaded".format(size))

    df: pd.DataFrame = open_xlsx(str(root) + path, "newcomerrecode")
    for i in range(len(df)):
        info = df.iloc[i]
        teacher = PrivateInfo.objects.get(username=info["teacher"])
        newcomer = PrivateInfo.objects.get(username=info["newcomer"])
        nr = NewcomerRecode(
            teacher=teacher,
            newcomer=newcomer,
            content=info["content"],
            commitTime=info["commitTime"]
        )
        nr.save()
    # logging.info("{} newcommer recode info loaded".format(len(NewcomerRecode.objects.all())))

    df: pd.DataFrame = open_xlsx(str(root) + path, "programtable")
    for i in range(len(df)):
        info = df.iloc[i]
        author = PrivateInfo.objects.get(username=info["author"])
        ProgramTable(
            id=str(info["id"]),
            name=info["name"],
            author=author,
            tag=info["tag"],
            contentCount=info["contentCount"],
            recommendTime=info["recommendTime"],
            audience=info["audience"],
            releaseTime=info["releaseTime"],
            isTemplate=info["isTemplate"],
        ).save()
    # logging.info("{} programs info loaded".format(len(ProgramTable.objects.all())))

    df: pd.DataFrame = open_xlsx(str(root) + path, "contenttable")
    for i in range(len(df)):
        info = df.iloc[i]
        author = PrivateInfo.objects.get(username=info["author"])
        program = ProgramTable.objects.get(id=info["programId"])
        ContentTable(
            id=info["id"],
            name=info["name"],
            author=author,
            intro=info["intro"],
            tag=info["tag"],
            isObligatory=info["isObligatory"],
            recommendedTime=info["recommendedTime"],
            audience=info["audience"],
            type=info["type"],
            isTemplate=info["isTemplate"],
            programId=program,
            releaseTime=info["releaseTime"],
            lessonCount=info["lessonCount"],
            beginTime=info["beginTime"],
            taskType=info["taskType"],
            text=info["text"],
            link=info["link"],
            questions=info['questions'],
            taskFile=info['taskFile']
        ).save()
    # logging.info("{} contents info loaded".format(len(ContentTable.objects.all())))

    df: pd.DataFrame = open_xlsx(str(root) + path, "lessontable")
    for i in range(len(df)):
        info = df.iloc[i]
        author = PrivateInfo.objects.get(username=info["author"])
        content = ContentTable.objects.get(id=info["content"])
        LessonTable(
            id=info["id"],
            name=info["name"],
            author=author,
            content=content,
            intro=info["intro"],
            recommendedTime=info["recommendedTime"],
            releaseTime=info["releaseTime"]
        ).save()
    # logging.info("{} lessons info loaded".format(len(LessonTable.objects.all())))
    df: pd.DataFrame = open_xlsx(str(root) + path, "coursewaretable")
    for i in range(len(df)):
        info = df.iloc[i]
        lesson = LessonTable.objects.get(id=info["lesson"])
        content = ContentTable.objects.get(id=info["content"])
        CoursewareTable(
            id=info["id"],
            lesson=lesson,
            content=content,
            name=info["name"],
            uploadTime=info["uploadTime"],
            url=info["url"]
        ).save()
    # logging.info("{} courseware info loaded".format(len(CoursewareTable.objects.all())))
    df: pd.DataFrame = open_xlsx(str(root) + path, "programcontenttable")
    for i in range(len(df)):
        info = df.iloc[i]
        program = ProgramTable.objects.get(id=info["program"])
        content = ContentTable.objects.get(id=info["content"])
        ProgramContentTable(
            program=program,
            content=content
        ).save()
    # logging.info("{} program content info loaded".format(len(ProgramContentTable.objects.all())))
    df: pd.DataFrame = open_xlsx(str(root) + path, "userprogramtable")
    for i in range(len(df)):
        info = df.iloc[i]
        user = PrivateInfo.objects.get(username=info["user"])
        program = ProgramTable.objects.get(id=info["program"])
        assigner = PrivateInfo.objects.get(username=info["assigner"])
        UserProgramTable(
            user=user,
            program=program,
            finishedContentCount=info["finishedContentCount"],
            finished=info["finished"],
            beginTime=info["beginTime"],
            endTime=info["endTime"],
            deadline=info["deadline"],
            assigner=assigner,
            score=info["score"]
        ).save()
    # logging.info("{} user program info loaded".format(len(UserProgramTable.objects.all())))

    df: pd.DataFrame = open_xlsx(str(root) + path, "usercontenttable")
    for i in range(len(df)):
        info = df.iloc[i]
        user = PrivateInfo.objects.get(username=info["user"])
        content = ContentTable.objects.get(id=info["content"])
        assigner = PrivateInfo.objects.get(username=info["assigner"])
        UserContentTable(
            user=user,
            content=content,
            finished=info["finished"],
            userBeginTime=info["userBeginTime"],
            userEndTime=info["userEndTime"],
            deadline=info["deadline"],
            assigner=assigner,
            isObligatory=info["isObligatory"],
            finishedLessonCount=info["finishedLessonCount"],
            examUsedTime=info["examUsedTime"],
            score=info["score"]
        ).save()
    # logging.info("{} user content info loaded".format(len(UserContentTable.objects.all())))
    df: pd.DataFrame = open_xlsx(str(root) + path, "userlessontable")
    for i in range(len(df)):
        info = df.iloc[i]
        user = PrivateInfo.objects.get(username=info["user"])
        lesson = LessonTable.objects.get(id=info["lesson"])
        UserLessonTable(
            user=user,
            lesson=lesson,
            beginTime=info['beginTime'],
            endTime=info["endTime"],
            finished=info["finished"]
        ).save()
    # logging.info("{} user lesson info loaded".format(len(UserLessonTable.objects.all())))
    df: pd.DataFrame = open_xlsx(str(root) + path, "notificationtable")
    for i in range(len(df)):
        info = df.iloc[i]
        NotificationTable(
            id=info["id"],
            author_name=info["author_name"],
            author_role=info["author_role"],
            author_username=info["author_username"],
            title=info["title"],
            content=info["content"],
            releaseTime=info["releaseTime"]
        ).save()

    df: pd.DataFrame = open_xlsx(str(root) + path, "grouptable")
    for i in range(len(df)):
        info = df.iloc[i]
        cr = PrivateInfo.objects.get(username=info["creator"])
        GroupTable(
            id=info["id"],
            name=info["name"],
            creator=cr
        ).save()
    df: pd.DataFrame = open_xlsx(str(root) + path, "usernotificationtable")
    for i in range(len(df)):
        info = df.iloc[i]
        user = PrivateInfo.objects.get(username=info["user"])
        noti = NotificationTable.objects.get(id=info["notification"])
        UserNotificationTable(
            user=user,
            notification=noti,
            finished=info["finished"]
        ).save()
    df: pd.DataFrame = open_xlsx(str(root) + path,"usergrouptable")
    for i in range(len(df)):
        info = df.iloc[i]
        group = GroupTable.objects.get(id=info["group"])
        user = PrivateInfo.objects.get(username=info["user"])
        UserGroupTable(
            user=user,
            group=group
        ).save()
    return gen_response(200, message="succefully write in")




def write_db2(req:HttpRequest):
    root = get_root_path()
    size = 100
    for i in range(size):
        pv = PrivateInfo(
            password=encrypt("Test@123"),
            username=f"user{i}",
            name=f"user{i}",
            city="北京",
            dept="测试部门",
            bio="用于测试的用户",
            joinDate="2022-5-1 23:59:59",
            joinStatus=PrivateInfo.EnumJoinStatus.OnJob,
            detail="detail",
            leader="admin",
            registrationDate="2022-5-1 23:59:59",
            employeeType=PrivateInfo.EnumEmployeeType.Social,
            avatar=str(root) + "/static/头像.jpeg",

            isAdmin=True,
            isTeacher=True,
            isHRBP=True,
            isNew=True,

            newcomerStartDate="2022-5-1 23:59:59",
            newcomerGraduateState=PrivateInfo.EnumNewcomerGraduateState.NotGraduate,
            newcomerGraduateDate="2022-5-1 23:59:59",

            historicalMembers=0,
            currentMembers=0,
            teacherNominationDate='2022-5-1 23:59:59',
            teacherExaminedStatus=PrivateInfo.EnumTeacherExaminedStatus.NotYet,
            teacherExaminedDate="2022-5-1 23:59:59",
            teacherIsDuty=False,
            teacherDutyDate="2022-5-1 23:59:59",
            teacherScore=0,
        )
        pv.save()
    return gen_response(200,message=f"successful write in {size} data!")
