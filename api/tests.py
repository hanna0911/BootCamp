"""
用于测试
"""
from django.test import TestCase
from utils.reader import *
import logging

logging.basicConfig(level=logging.DEBUG)


# Create your tests here.

class Tests(TestCase):

    def setUp(self):
        self.session = {}
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

    def request(self, case: dict):
        req = case["request"]
        validate = case["validate"]
        logging.info(case["name"])
        if req["method"].lower() == "post":
            logging.debug("posting url: {}".format(req["url"]))
            res = self.client.post(req["url"], data=req["data"], content_type="application/json")
        elif req["method"].lower() == "get":
            logging.debug("getting url: {}".format(req["url"]))
            res = self.client.get(req["url"], data=req["data"], content_type="application/json")
        else:
            logging.debug("invalid method")
            return None
        for i in range(len(validate)):
            if "equals" in validate[i].keys():
                equ_assert = validate[i]["equals"]
                if "status_code" in equ_assert.keys():
                    logging.debug("status code:{}  message:{}".format(res.status_code, res.json()["message"]))
                    self.assertEqual(res.status_code, equ_assert["status_code"])
                    logging.info("OK")
        if "type" in case.keys():
            task_type = case["type"]
            if task_type == "session":
                logging.error(res.body["SessionID"])
                self.session[req["username"]] = res.headers["SessionID"]

    # def test_join(self):
    #     self.process("/testcase/join.yml")
    #
    # def test_login(self):
    #     self.process("/testcase/login.yml")

    def test_get_session(self):
        self.process("/testcase/get_session.yml")

    def test_ok(self):
        assert 1, 1
