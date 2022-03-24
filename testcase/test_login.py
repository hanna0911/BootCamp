"""
测试登录
"""
import pytest
from utils.engine import my_engine

# import requests
# from requests import Response
# from requests import request
# from api.models import PrivateInfo

class TestLogin:
    def test_login(self):
        my_engine.test("/testcase/test.yml")

#
# def setup_module():
#     user = PrivateInfo.objects.create(name="test", userid="testid",
#                                       password="8776f108e247ab1e2b323042c049c266407c81fbad41bde1e8dfc1bb66fd267e",
#                                       city="北京", dept="管理部门")
#     user.save()
#
#
# class Client:
#     def __init__(self, baseurl: str):
#         self.base = baseurl
#
#     def post(self, path: str, data: dict):
#         return requests.post(self.base + path, json=data)
#
#     def get(self, path: str, data: dict):
#         return requests.get(self.base + path, json=data)
#
#
# class TestLogin:
#     def assertEqual(self, a, b):
#         assert(a==b)
#
#     def __init__(self):
#         self.client = Client("https://backend-wewritebugs.app.secoder.net/")
#
#     def test_login_success(self):
#         post_data = {
#             "username": "testid",
#             "password": "8776f108e247ab1e2b323042c049c266407c81fbad41bde1e8dfc1bb66fd267e"
#         }
#         response = self.client.post("/login", data=post_data)
#         self.assertEqual(200, response.status_code)
#
#     def test_login_password_error(self):
#         post_data = {
#             "username": "testid",
#             "password": "1233"
#         }
#         response = self.client.post("/login", data=post_data)
#         self.assertEqual(400, response.status_code)
#
#     def test_login_not_found(self):
#         post_data = {
#             "username": "td",
#             "password": "1233"
#         }
#         response = self.client.post("/login", data=post_data)
#         self.assertEqual(400, response.status_code)
#
#     def test_join_duplicate(self):
#         post_data = {
#             "username": "testid",
#             "password": "1234",
#             "personal_info": {
#                 "city": "北京"
#             }
#         }
#         response = self.client.post("/join", data=post_data)
#         self.assertEqual(400, response.status_code)
#
#     def test_join_success(self):
#         post_data = {
#             "username": "test12",
#             "password": "1234",
#             "personal_info": {
#                 "city": "北京",
#                 "name": "摆烂",
#                 "department": "管理部门"
#             }
#         }
#         response = self.client.post("/join", data=post_data)
#         self.assertEqual(200, response.status_code)
