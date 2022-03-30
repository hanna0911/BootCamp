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
                    yield case
                else:
                    print("错误的yml文件,请确认是否有name,request,validate 等字段")
            else:
                print("错误的yml文件,请确认是否有name,request,validate 等字段")
    except Exception as e:
        print("读取出错,异常信息:{}".format(traceback.format_exc()))


def create_data_yml(path: str):
    infos = read_testcase_yaml(path)
    for info in infos:
        if info["classname"].lower() == "privateinfo":
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

                newcomerStartDate=info["newcomerStartDate"],
                newcomerIsGraduate=info["newcomerIsGraduate"],
                newcomerGraduateDate=info["newcomerGraduateDate"],

                historicalMembers=info["historicalMembers"],
                currentMembers=info["currentMembers"],
                teacherNominationDate=info["teacherNominationDate"],
                teacherExaminedStatus=info["teacherExaminedStatus"],
                teacherExaminedDate=info["teacherExaminedDate"],
                teacherIsDuty=info["teacherIsDuty"],
                teacherDutyDate=info["teacherDutyDate"],
                teacherScore=info["teacherScore"],
            )
        elif info["classname"].lower() == "program":
            author = PrivateInfo.objects.get(username__exact=info['author'])
            ProgramTable.objects.create(
                id=info["id"],
                name=info["name"],
                author=author,
                intro=info["intro"],
                tag=info["tag"],
                contentCount=info["contentCount"],
                audience=info["audience"],
                recommendTime=info["recommendTime"]
            )

    if __name__ == '__main__':
        info = read_testcase_yaml("/testcase/test.yml")
        gen = analysis_parameters(info)
        next(gen)


def create_data_xlsx(path: str):
    # def write_db(path: str, model):
    #     root = get_root_path()
    #     df: pd.DataFrame = open_xlsx(str(root) + path, "privateinfo")
    #
    #     for i in range(len(df)):
    #         info = df.iloc[i]
    #         content
    #         for j in
    #     PrivateInfo.objects.create(
    #         "paidhg", "username"
    #     )

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
