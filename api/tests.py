"""
用于测试
"""
import pytest
from django.test import TestCase, Client
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from utils.reader import *
import logging

logging.basicConfig(level=logging.DEBUG)

# Create your tests here.

sessions = {}

Clients = {
    'admin': Client(),
    "HRBP": Client(),
    "teacher": Client(),
    "newcomer": Client()
}


class Tests(TestCase):
    def setUp(self):
        create_data_yml("/testcase/init_data.yml")
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

    def process(self, path: str):
        case_info = read_testcase_yaml(path)
        gen = analysis_parameters(case_info)
        while True:
            try:
                case = next(gen)
                self.request(case)
            except StopIteration as e:
                print('Generator return value:', e.value)
                break

    def get_response(self, req: dict) -> JsonResponse:
        if req["method"].lower() == "post":
            logging.debug("posting url: {}".format(req["url"]))
            res = self.client.post(req["url"], data=req["data"], content_type="application/json")
            return res
        elif req["method"].lower() == "get":
            logging.debug("getting url: {}".format(req["url"]))
            res = self.client.get(req["url"], data=req["data"], content_type="application/json")
            return res
        else:
            logging.debug("invalid method")
            raise Exception("invalid method")

    def validate(self, validate, res):
        for i in range(len(validate)):
            if "equals" in validate[i].keys():
                equ_assert = validate[i]["equals"]
                if "status_code" in equ_assert.keys():
                    logging.debug("status code:{}  message:{}".format(res.status_code, res.json()["message"]))
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

    def test_join(self):
        self.process("/testcase/join.yml")

    def test_login(self):
        self.process("/testcase/login.yml")
    @pytest.mark.run('first')
    def test_get_session(self):
        self.process("/testcase/get_session.yml")

    def test_switch_role(self):
        self.process("/testcase/switch_role.yml")
