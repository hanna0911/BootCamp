"""
提供api进行数据库的写入
"""
from django.http import HttpRequest
from models import *


def write_db(req: HttpRequest):
    path = "/testcase/template.xlsx"
    root = get_root_path()
    df: pd.DataFrame = open_xlsx(str(root) + path, "privateinfo")
    for i in range(len(df)):
        info = df.iloc[i]
        PrivateInfo.objects.create(
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
            registrationDate=info["registrationDate"],
            employeeType=info["employeeType"],

            isAdmin=info["isAdmin"],
            isTeacher=info["isTeacher"],
            isHRBP=info["isHRBP"],
            isNew=info["isNew"],

            newcomerStartDate=str(info["newcomerStartDate"]),
            newcomerIsGraduate=info["newcomerIsGraduate"],
            newcomerGraduateDate=str(info["newcomerGraduateDate"]),

            historicalMembers=info["historicalMembers"],
            currentMembers=info["currentMembers"],
            teacherNominationDate=info["teacherNominationDate"],
            teacherExaminedStatus=info["teacherExaminedStatus"],
            teacherExaminedDate=info["teacherExaminedDate"],
            teacherIsDuty=info["teacherIsDuty"],
            teacherDutyDate=info["teacherDutyDate"],
            teacherScore=info["teacherScore"],
        )
    size = len(PrivateInfo.objects.all())
    logging.info("{} private info loaded".format(size))

    df: pd.DataFrame = open_xlsx(str(root) + path, "teachernewcomertable")
    for i in range(len(df)):
        info = df.iloc[i]
        teacher = PrivateInfo.objects.get(username=info["teacher"])
        newcomer = PrivateInfo.objects.get(username=info["newcomer"])
        TeacherNewcomerTable.objects.create(
            newcomer=newcomer,
            teacher=teacher,
            teacherScore=info["teacherScore"],
            newcomerToTeacher=info["newcomerToTeacher"],
            newcomerScore=info["newcomerScore"],
            teacherToNewcomer=info["teacherToNewcomer"]
        )
    size = len(TeacherNewcomerTable.objects.all())
    logging.info("{} teacher newcomer info loaded".format(size))

    df: pd.DataFrame = open_xlsx(str(root) + path, "newcomerrecode")
    for i in range(len(df)):
        info = df.iloc[i]
        teacher = PrivateInfo.objects.get(username=info["teacher"])
        newcomer = PrivateInfo.objects.get(username=info["newcomer"])
        NewcomerRecode.objects.create(
            teacher=teacher,
            newcomer=newcomer,
            content=info["content"],
            commitTime=info["commitTime"]
        )
    logging.info("{} newcommer recode info loaded".format(len(NewcomerRecode.objects.all())))

    df: pd.DataFrame = open_xlsx(str(root) + path, "programtable")
    for i in range(len(df)):
        info = df.iloc[i]
        author = PrivateInfo.objects.get(username=info["author"])
        ProgramTable.objects.create(
            id=str(info["id"]),
            name=info["name"],
            author=author,
            tag=info["tag"],
            contentCount=info["contentCount"],
            recommendTime=info["recommendTime"],
            audience=info["audience"],
            releaseTime=info["releaseTime"]
        )
    logging.info("{} programs info loaded".format(len(ProgramTable.objects.all())))

    df: pd.DataFrame = open_xlsx(str(root) + path, "contenttable")
    for i in range(len(df)):
        info = df.iloc[i]
        author = PrivateInfo.objects.get(username=info["author"])
        program = ProgramTable.objects.get(id=info["programId"])
        ContentTable.objects.create(
            id=info["id"],
            name=info["name"],
            author=author,
            intro=info["intro"],
            tag=info["tag"],
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
            link=info["link"]
        )
    logging.info("{} contents info loaded".format(len(ContentTable.objects.all())))

    df: pd.DataFrame = open_xlsx(str(root) + path, "lessontable")
    for i in range(len(df)):
        info = df.iloc[i]
        author = PrivateInfo.objects.get(username=info["author"])
        content = ContentTable.objects.get(id=info["content"])
        LessonTable.objects.create(
            id=info["id"],
            name=info["name"],
            author=author,
            content=content,
            intro=info["intro"],
            recommendedTime=info["recommendedTime"],
            releaseTime=info["releaseTime"]
        )
    logging.info("{} lessons info loaded".format(len(LessonTable.objects.all())))
    df: pd.DataFrame = open_xlsx(str(root) + path, "coursewaretable")
    for i in range(len(df)):
        info = df.iloc[i]
        lesson = LessonTable.objects.get(id=info["lesson"])
        content = ContentTable.objects.get(id=info["content"])
        CoursewareTable.objects.create(
            id=info["id"],
            lesson=lesson,
            content=content,
            name=info["name"],
            uploadTime=info["uploadTime"],
            url=info["url"]
        )
    logging.info("{} courseware info loaded".format(len(CoursewareTable.objects.all())))
    df: pd.DataFrame = open_xlsx(str(root) + path, "programcontenttable")
    for i in range(len(df)):
        info = df.iloc[i]
        program = ProgramTable.objects.get(id=info["program"])
        content = ContentTable.objects.get(id=info["content"])
        ProgramContentTable.objects.create(
            program=program,
            content=content
        )
    logging.info("{} program content info loaded".format(len(ProgramContentTable.objects.all())))
    df: pd.DataFrame = open_xlsx(str(root) + path, "userprogramtable")
    for i in range(len(df)):
        info = df.iloc[i]
        user = PrivateInfo.objects.get(username=info["user"])
        program = ProgramTable.objects.get(id=info["program"])
        assigner = PrivateInfo.objects.get(username=info["assigner"])
        UserProgramTable.objects.create(
            user=user,
            program=program,
            finishedContentCount=info["finishedContentCount"],
            finished=info["finished"],
            beginTime=info["beginTime"],
            endTime=info["endTime"],
            deadline=info["deadline"],
            assigner=assigner,
            score=info["score"]
        )
    logging.info("{} user program info loaded".format(len(UserProgramTable.objects.all())))
