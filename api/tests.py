"""
用于测试
"""
from django.test import TestCase
from utils.reader import *
import logging


# Create your tests here.

class Tests(TestCase):
    def setUp(self):
        create_data("/testcase/init_data.yml")

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

    def request(self, case: dict):
        req = case["request"]
        validate = case["validate"]
        if req["method"].lower() == "post":
            logging.info("posting url: {}".format(req["url"]))
            res = self.client.post(req["url"], data=req["data"], content_type="application/json")
        elif req["method"].lower() == "get":
            logging.info("getting url: {}".format(req["url"]))
            res = self.client.get(req["url"], data=req["data"], content_type="application/json")
        else:
            print("error, invalid method!")
            return None
        for i in range(len(validate)):
            if "equals" in validate[i].keys():
                equ_assert = validate[i]["equals"]
                if "status_code" in equ_assert.keys():
                    print(res.status_code)
                    assert res.status_code == equ_assert["status_code"]

    def test_join(self):
        self.process("/testcase/join.yml")

    def test_login(self):
        self.process("/testcase/login.yml")
