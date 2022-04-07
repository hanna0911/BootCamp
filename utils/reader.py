import logging
import traceback
from pathlib import Path
import yaml
from api.models import *
from api.api_util import encrypt
import pandas as pd
import os
from django.db.models import Model


def get_root_path():
    return Path(__file__).resolve().parent.parent


def read_testcase_yaml(path: str):
    try:
        with open(str(get_root_path()) + path, 'r', encoding='utf-8') as f:
            info = yaml.load(f.read(), yaml.FullLoader)
            return info
    except Exception as e:
        print("读取出错,异常信息:{}".format(traceback.format_exc()))


def open_xlsx(path: str, sheet_name):
    try:
        df = pd.read_excel(path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print("读取错误")
        raise e


def analysis_parameters(info: list):
    try:
        for case in info:
            if "name" in case.keys() and 'request' in case.keys() and 'validate' in case.keys():
                req = case["request"]
                if "method" in req.keys() and "url" in req.keys() and "data" in req.keys():
                    if req["url"] == "/login" or req["url"] == "/join" or req[
                        "url"] == "/write_db" or "ident" in case.keys():
                        yield case
                    else:
                        logging.error("非注册登录路由下未指定ident字段")
                else:
                    logging.error("错误的yml文件,请确认是否有name,request,validate 等字段")
            else:
                logging.error("错误的yml文件,请确认是否有name,request,validate 等字段")
    except Exception as e:
        logging.error("读取出错,异常信息:{}".format(traceback.format_exc()))


# def create_data_yml(path: str):
#     infos = read_testcase_yaml(path)
#     for info in infos:
#         if info["classname"].lower() == "privateinfo":
#             PrivateInfo.objects.create(
#                 password=encrypt(info["password"]),
#                 username=info["username"],
#
#                 name=info["name"],
#                 city=info["city"],
#                 dept=info["dept"],
#                 bio=info["bio"],
#                 joinDate=info["joinDate"],
#                 joinStatus=info["joinStatus"],
#                 detail=info["detail"],
#                 leader=info["leader"],
#                 registrationDate=info["registrationDate"],
#                 employeeType=info["employeeType"],
#
#                 isAdmin=info["isAdmin"],
#                 isTeacher=info["isTeacher"],
#                 isHRBP=info["isHRBP"],
#                 isNew=info["isNew"],
#
#                 newcomerStartDate=info["newcomerStartDate"],
#                 newcomerIsGraduate=info["newcomerIsGraduate"],
#                 newcomerGraduateDate=info["newcomerGraduateDate"],
#
#                 historicalMembers=info["historicalMembers"],
#                 currentMembers=info["currentMembers"],
#                 teacherNominationDate=info["teacherNominationDate"],
#                 teacherExaminedStatus=info["teacherExaminedStatus"],
#                 teacherExaminedDate=info["teacherExaminedDate"],
#                 teacherIsDuty=info["teacherIsDuty"],
#                 teacherDutyDate=info["teacherDutyDate"],
#                 teacherScore=info["teacherScore"],
#             )
#         elif info["classname"].lower() == "program":
#             author = PrivateInfo.objects.get(username__exact=info['author'])
#             ProgramTable.objects.create(
#                 id=info["id"],
#                 name=info["name"],
#                 author=author,
#                 intro=info["intro"],
#                 tag=info["tag"],
#                 contentCount=info["contentCount"],
#                 audience=info["audience"],
#                 recommendTime=info["recommendTime"]
#             )


# def create_data_xlsx(path: str):
#     root = get_root_path()
#     df: pd.DataFrame = open_xlsx(str(root) + path, "privateinfo")
#     for i in range(len(df)):
#         info = df.iloc[i]
#         PrivateInfo.objects.create(
#             password=encrypt(info["password"]),
#             username=info["username"],
#
#             name=info["name"],
#             city=info["city"],
#             dept=info["dept"],
#             bio=info["bio"],
#             joinDate=info["joinDate"],
#             joinStatus=info["joinStatus"],
#             detail=info["detail"],
#             leader=info["leader"],
#             registrationDate=info["registrationDate"],
#             employeeType=info["employeeType"],
#
#             isAdmin=info["isAdmin"],
#             isTeacher=info["isTeacher"],
#             isHRBP=info["isHRBP"],
#             isNew=info["isNew"],
#
#             newcomerStartDate=str(info["newcomerStartDate"]),
#             newcomerIsGraduate=info["newcomerIsGraduate"],
#             newcomerGraduateDate=str(info["newcomerGraduateDate"]),
#
#             historicalMembers=info["historicalMembers"],
#             currentMembers=info["currentMembers"],
#             teacherNominationDate=info["teacherNominationDate"],
#             teacherExaminedStatus=info["teacherExaminedStatus"],
#             teacherExaminedDate=info["teacherExaminedDate"],
#             teacherIsDuty=info["teacherIsDuty"],
#             teacherDutyDate=info["teacherDutyDate"],
#             teacherScore=info["teacherScore"],
#         )
#     size = len(PrivateInfo.objects.all())
#     logging.info("{} private info loaded".format(size))
#
#     df: pd.DataFrame = open_xlsx(str(root) + path, "teachernewcomertable")
#     for i in range(len(df)):
#         info = df.iloc[i]
#         teacher = PrivateInfo.objects.get(username=info["teacher"])
#         newcomer = PrivateInfo.objects.get(username=info["newcomer"])
#         TeacherNewcomerTable.objects.create(
#             newcomer=newcomer,
#             teacher=teacher,
#             teacherScore=info["teacherScore"],
#             newcomerToTeacher=info["newcomerToTeacher"],
#             newcomerScore=info["newcomerScore"],
#             teacherToNewcomer=info["teacherToNewcomer"]
#         )
#     size = len(TeacherNewcomerTable.objects.all())
#     logging.info("{} teacher newcomer info loaded".format(size))
#
#     df: pd.DataFrame = open_xlsx(str(root) + path, "newcomerrecode")
#     for i in range(len(df)):
#         info = df.iloc[i]
#         teacher = PrivateInfo.objects.get(username=info["teacher"])
#         newcomer = PrivateInfo.objects.get(username=info["newcomer"])
#         NewcomerRecode.objects.create(
#             teacher=teacher,
#             newcomer=newcomer,
#             content=info["content"],
#             commitTime=info["commitTime"]
#         )
#     logging.info("{} newcommer recode info loaded".format(len(NewcomerRecode.objects.all())))
#
#     df: pd.DataFrame = open_xlsx(str(root) + path, "programtable")
#     for i in range(len(df)):
#         info = df.iloc[i]
#         author = PrivateInfo.objects.get(username=info["author"])
#         ProgramTable.objects.create(
#             id=str(info["id"]),
#             name=info["name"],
#             author=author,
#             tag=info["tag"],
#             contentCount=info["contentCount"],
#             recommendTime=info["recommendTime"],
#             audience=info["audience"],
#             releaseTime=info["releaseTime"]
#         )
#     logging.info("{} programs info loaded".format(len(ProgramTable.objects.all())))
#
#     df: pd.DataFrame = open_xlsx(str(root) + path, "contenttable")
#     for i in range(len(df)):
#         info = df.iloc[i]
#         author = PrivateInfo.objects.get(username=info["author"])
#         program = ProgramTable.objects.get(id=info["programId"])
#         ContentTable.objects.create(
#             id=info["id"],
#             name=info["name"],
#             author=author,
#             intro=info["intro"],
#             tag=info["tag"],
#             recommendedTime=info["recommendedTime"],
#             audience=info["audience"],
#             type=info["type"],
#             isTemplate=info["isTemplate"],
#             programId=program,
#             releaseTime=info["releaseTime"],
#             lessonCount=info["lessonCount"],
#             beginTime=info["beginTime"],
#             taskType=info["taskType"],
#             text=info["text"],
#             link=info["link"]
#         )
#     logging.info("{} contents info loaded".format(len(ContentTable.objects.all())))
#
#     df: pd.DataFrame = open_xlsx(str(root) + path, "lessontable")
#     for i in range(len(df)):
#         info = df.iloc[i]
#         author = PrivateInfo.objects.get(username=info["author"])
#         content = ContentTable.objects.get(id=info["content"])
#         LessonTable.objects.create(
#             id=info["id"],
#             name=info["name"],
#             author=author,
#             content=content,
#             intro=info["intro"],
#             recommendedTime=info["recommendedTime"],
#             releaseTime=info["releaseTime"]
#         )
#     logging.info("{} lessons info loaded".format(len(LessonTable.objects.all())))
#     df: pd.DataFrame = open_xlsx(str(root) + path, "coursewaretable")
#     for i in range(len(df)):
#         info = df.iloc[i]
#         lesson = LessonTable.objects.get(id=info["lesson"])
#         content = ContentTable.objects.get(id=info["content"])
#         CoursewareTable.objects.create(
#             id=info["id"],
#             lesson=lesson,
#             content=content,
#             name=info["name"],
#             uploadTime=info["uploadTime"],
#             url=info["url"]
#         )
#     logging.info("{} courseware info loaded".format(len(CoursewareTable.objects.all())))
#     df: pd.DataFrame = open_xlsx(str(root) + path, "programcontenttable")
#     for i in range(len(df)):
#         info = df.iloc[i]
#         program = ProgramTable.objects.get(id=info["program"])
#         content = ContentTable.objects.get(id=info["content"])
#         ProgramContentTable.objects.create(
#             program=program,
#             content=content
#         )
#     logging.info("{} program content info loaded".format(len(ProgramContentTable.objects.all())))
#     df: pd.DataFrame = open_xlsx(str(root) + path, "userprogramtable")
#     for i in range(len(df)):
#         info = df.iloc[i]
#         user = PrivateInfo.objects.get(username=info["user"])
#         program = ProgramTable.objects.get(id=info["program"])
#         assigner = PrivateInfo.objects.get(username=info["assigner"])
#         UserProgramTable.objects.create(
#             user=user,
#             program=program,
#             finishedContentCount=info["finishedContentCount"],
#             finished=info["finished"],
#             beginTime=info["beginTime"],
#             endTime=info["endTime"],
#             deadline=info["deadline"],
#             assigner=assigner,
#             score=info["score"]
#         )
#     logging.info("{} user program info loaded".format(len(UserProgramTable.objects.all())))
#
#     df: pd.DataFrame = open_xlsx(str(root) + path, "usercontenttable")
#     for i in range(len(df)):
#         info = df.iloc[i]
#         user = PrivateInfo.objects.get(username=info["user"])
#         content = ContentTable.objects.get(id=info["content"])
#         assigner = PrivateInfo.objects.get(username=info["assigner"])
#         UserContentTable.objects.create(
#             user=user,
#             content=content,
#             finished=info["finished"],
#             userBeginTime=info["userBeginTime"],
#             userEndTime=info["userEndTime"],
#             deadline=info["deadline"],
#             assigner=assigner,
#             isObligatory=info["isObligatory"],
#             finishedLessonCount=info["finishedLessonCount"],
#             examUsedTime=info["examUsedTime"],
#             score=info["score"]
#         )
#     logging.info("{} user content info loaded".format(len(UserContentTable.objects.all())))
#     df: pd.DataFrame = open_xlsx(str(root) + path, "userlessontable")
#     for i in range(len(df)):
#         info = df.iloc[i]
#         user = PrivateInfo.objects.get(username=info["user"])
#         lesson = LessonTable.objects.get(id=info["lesson"])
#         UserLessonTable.objects.create(
#             user=user,
#             lesson=lesson,
#             beginTime=info['beginTime'],
#             endTime=info["endTime"],
#             finished=info["finished"]
#         )
#     logging.info("{} user lesson info loaded".format(len(UserLessonTable.objects.all())))


def create_templage_xlsx(path: str):
    def save(writer: pd.ExcelWriter, model, sheet_name: str):
        info = model._meta.fields
        info_list = [info[i].name for i in range(len(info))]
        info_dict = {}
        for i in range(1, len(info_list)):
            info_dict[info_list[i]] = []
        private_data = pd.DataFrame(info_dict)
        private_data.to_excel(writer, sheet_name=sheet_name)

    writer = pd.ExcelWriter(path)
    save(writer, PrivateInfo, PrivateInfo._meta.model_name)
    save(writer, Honor, Honor._meta.model_name)
    save(writer, TeacherNewcomerTable, TeacherNewcomerTable._meta.model_name)
    save(writer, NewcomerRecode, NewcomerRecode._meta.model_name)
    save(writer, ProgramTable, ProgramTable._meta.model_name)
    save(writer, ContentTable, ContentTable._meta.model_name)
    save(writer, LessonTable, LessonTable._meta.model_name)
    save(writer, CoursewareTable, CoursewareTable._meta.model_name)
    save(writer, ProgramContentTable, ProgramContentTable._meta.model_name)
    save(writer, UserProgramTable, UserProgramTable._meta.model_name)
    save(writer, UserContentTable, UserContentTable._meta.model_name)
    save(writer, UserLessonTable, UserLessonTable._meta.model_name)

    writer.save()
    writer.close()
