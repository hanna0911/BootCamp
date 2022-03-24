"""
用于测试远程服务的引擎
"""
from requests import request
from utils.reader import read_testcase_yaml, analysis_parameters


class Engine:
    def __init__(self):
        # self.baseurl = "http://backend-wewritebugs.app.secoder.net"
        self.baseurl = "http://127.0.0.1:8000"
        self.proxies = {
            "http": None,
            "https": None,
        }
        # request(method="GET", url=self.baseurl + "/init",  proxies=self.proxies)

    def test(self, path: str):
        case_info = read_testcase_yaml(path)
        gen = analysis_parameters(case_info)
        while True:
            try:
                case = next(gen)
                self.run(case)
            except StopIteration as e:
                print('Generator return value:', e.value)
                break

    def run(self, case):
        req = case["request"]
        validate = case["validate"]
        res = request(method=req["method"],
                      url=self.baseurl + req['url'],
                      json=req["data"], proxies=self.proxies)

        for i in range(len(validate)):
            if "equals" in validate[i].keys():
                equ_assert = validate[i]["equals"]
                if "status_code" in equ_assert.keys():
                    print(res.status_code, res.text)
                    assert res.status_code == equ_assert["status_code"]


my_engine = Engine()
