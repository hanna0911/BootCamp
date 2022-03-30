import traceback
from pathlib import Path
import yaml
from api.models import *


def get_root_path():
    return Path(__file__).resolve().parent.parent


def read_testcase_yaml(path: str):
    try:
        with open(str(get_root_path()) + path, 'r', encoding='utf-8') as f:
            info = yaml.load(f.read(), yaml.FullLoader)
            return info
    except Exception as e:
        print("读取出错,异常信息:{}".format(traceback.format_exc()))


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


def create_data(path: str):
    infos = read_testcase_yaml(path)
    for info in infos:
        if info["classname"].lower() == "privateinfo":
            PrivateInfo.objects.create(
                password=info["password"],
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
