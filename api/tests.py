"""
用于测试
"""
import pytest
from django.test import TestCase, Client
from django.http import JsonResponse
from utils.reader import *
import logging

logging.basicConfig(level=logging.DEBUG)

# Create your tests here.

sessions = {}



class Tests(TestCase):
    def setUp(self):
        # create_data_yml("/testcase/init_data.yml")
        self.process("/testcase/write_db.yml")
        # create_data_xlsx("/testcase/template.xlsx")

    def login(self, ident):
        if ident == "admin":
            self.process("/testcase/idents/admin.yml")
        elif ident.lower() == "hrbp":
            self.process("/testcase/idents/HRBP.yml")
        elif ident == "teacher":
            self.process("/testcase/idents/teacher.yml")
        elif ident == "newcomer":
            self.process("/testcase/idents/newcomer.yml")
        else:
            raise Exception("wrong ident")

    def process(self, path: str):
        case_info = read_testcase_yaml(path)
        gen = analysis_parameters(case_info)
        while True:
            try:
                case = next(gen)
                self.request(case)
            except StopIteration as e:
                break

    def get_response(self, req: dict) -> JsonResponse:
        if req["method"].lower() == "post":
            logging.debug("posting url: {}".format(req["url"]))
            res = self.client.post("/api" + req["url"], data=req["data"], content_type="application/json")
            return res
        elif req["method"].lower() == "get":
            logging.debug("getting url: {}".format(req["url"]))
            res = self.client.get("/api" + req["url"], data=req["data"], content_type="application/json")
            return res
        else:
            logging.debug("invalid method")
            raise Exception("invalid method")

    def validate(self, validate, res):
        for i in range(len(validate)):
            if "equals" in validate[i].keys():
                equ_assert = validate[i]["equals"]
                if "status_code" in equ_assert.keys():
                    if res.headers['Content-Type'] == "application/json":
                        logging.debug("status code:{}  message:{}".format(res.status_code, res.json()["message"]))
                    elif res.headers['Content-Type'] == "text/html":
                        logging.debug("status code{} text/html format".format(res.status_code))
                    self.assertEqual(res.status_code, equ_assert["status_code"])
                    logging.info("OK")

    def request(self, case: dict):
        self.client.cookies.clear()
        req = case["request"]
        validate = case["validate"]
        logging.info(case["name"])
        if "type" in case.keys():
            task_type = case["type"]
            if task_type == "sessions":
                res = self.get_response(req)
                self.validate(validate, res)
        elif "ident" in case.keys():
            # logging.warning("ident")
            ident_list = case["ident"]
            for ident in ident_list:
                # 遍历所有身份进行请求
                self.login(ident)
                res = self.get_response(req)
                self.validate(validate, res)
        else:
            self.validate(validate, self.get_response(req))

    def test_blanck(self):
        assert 1, 1

    def test_get_token(self):
        self.process("/testcase/get_token.yml")

    def test_write_db(self):
        PrivateInfo.objects.all().delete()
        Honor.objects.all().delete()
        TeacherNewcomerTable.objects.all().delete()
        NewcomerRecode.objects.all().delete()
        ProgramTable.objects.all().delete()
        ContentTable.objects.all().delete()
        LessonTable.objects.all().delete()
        CoursewareTable.objects.all().delete()
        ProgramContentTable.objects.all().delete()
        UserProgramTable.objects.all().delete()
        UserContentTable.objects.all().delete()
        UserLessonTable.objects.all().delete()
        self.process("/testcase/write_db.yml")

    def test_join(self):
        self.process("/testcase/join.yml")

    def test_login(self):
        self.process("/testcase/login.yml")

    def test_switch_role(self):
        self.process("/testcase/switch_role.yml")

    # def test_teacher_wait_list(self):
    #     self.process("/testcase/teacher_wait_list.yml")

    # def test_duty_teacher_list(self):
    #     self.process("/testcase/duty_teacher_list.yml")

    # def test_admin_newcomer_list(self):
    #     self.process("/testcase/admin_newcomer_list.yml")

    # def test_nominate_process(self):
    #     self.process("/testcase/nominate_process.yml")

    # def test_get_user_info(self):
    #     self.process("/testcase/get_user_info.yml")

    # def test_logout(self):
    #     self.process("/testcase/logout.yml")

    # def test_nominated_list(self):
    #     self.process("/testcase/nominated_list.yml")

    # def test_get_newcomer_info(self):
    #     self.process("/testcase/get_newcomer_info.yml")

    # def test_nominate_accept_reject(self):
    #     self.process("/testcase/nominate_accept_reject.yml")

    # def test_assign_teacher(self):
    #     self.process("/testcase/assign_teacher.yml")

    # def test_upload_program(self):
    #     self.process("/testcase/upload_program.yml")

    # # def test_upload_content_template(self):
    # #     self.process("/testcase/upload_content_template.yml")

    # def test_upload_lesson_template(self):
    #     self.process("/testcase/upload_lesson_template.yml")

    # def test_video(self):
    #     logging.info("测试video接口")
    #     res = self.client.get("/api/video")
    #     assert res.status_code, 200

    # def test_avatar_and_by_name(self):
    #     self.process("/testcase/avatar.yml")

    # def test_teacher_newcomer_list(self):
    #     self.process("/testcase/teacher_newcomer_list.yml")

    # def test_get_honor(self):
    #     self.process("/testcase/get_honor.yml")

    # def test_teacher_summary_info(self):
    #     self.process("/testcase/teacher_summary_info.yml")

    # def test_nominate_teachers(self):
    #     self.process("/testcase/nominate_teachers.yml")

    # def test_content_list_apis(self):
    #     self.process("/testcase/content_list.yml")

    # def test_assign_content(self):
    #     self.process("/testcase/assign_content.yml")

    def test_bootcamp_attend(self):
        self.process("/testcase/bootcamp_attend.yml")

    def test_newcomer_average_score(self):
        self.process("/testcase/newcomer_average_score.yml")

    def test_teacher_average_score(self):
        self.process("/testcase/teacher_average_score.yml")

    def test_camp_completion(self):
        self.process("/testcase/camp_completion.yml")

    def test_graduate_time(self):
        self.process("/testcase/graduate_time.yml")

    def test_tutor_assignment_chart(self):
        self.process("/testcase/tutor_assignment_chart.yml")
