"""
用于测试
"""
import json

import pytest
from django.test import TestCase
from utils.reader import *
import logging

logging.basicConfig(level=logging.DEBUG)

# Create your tests here.

sessions = {}


class Tests(TestCase):
    def setUp(self):
        create_data_yml("/testcase/init_data.yml")
        # create_data_xlsx("/testcase/template.xlsx")

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

    def get_response(self, req):
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
                str_list = str(self.client.cookies.get("SessionID")).split()
                session_id = str_list[1].replace("SessionID=", "").replace(";", "")
                logging.error(session_id)
                sessions[req['data']["username"]] = session_id
        if "ident" in case.keys():
            ident_list = case["ident"]
            for ident in ident_list:
                # 遍历所有身份进行请求
                self.client.cookies.clear()
                self.client.cookies["SessionID"] = sessions[ident]
                logging.error(self.client.cookies)
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

    # def test_switch_role(self):
    #     self.process("/testcase/switch_role.yml")
