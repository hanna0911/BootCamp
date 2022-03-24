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
                name=info["name"],
                city=info["city"],
                dept=info["dept"],
                password=info["password"],
                username=info["username"],
                bio=info["bio"],
                entryTime=info["entryTime"],
                employeeType=info["employeeType"],
                graduationTime=info["graduationTime"],
                superior=info["superior"],
                detail=info["detail"],
                historicalMembers=info["historicalMembers"],
                currentMembers=info["currentMembers"],
                isAdmin=info["isAdmin"],
                isTeacher=info["isTeacher"],
                isHRBP=info["isHRBP"],
                isNew=info["isNew"]
            )


if __name__ == '__main__':
    info = read_testcase_yaml("/testcase/test.yml")
    gen = analysis_parameters(info)
    next(gen)
