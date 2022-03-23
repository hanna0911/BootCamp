"""
用于测试
"""
from django.test import TestCase
from .models import PrivateInfo


# Create your tests here.

class MessageModelTests(TestCase):
    def setUp(self):
        user = PrivateInfo.objects.create(name="test", userid="testid",
                                          password="8776f108e247ab1e2b323042c049c266407c81fbad41bde1e8dfc1bb66fd267e",
                                          city="北京", dept="管理部门")
        user.save()

    def test_login_success(self):
        post_data = {
            "username": "testid",
            "password": "8776f108e247ab1e2b323042c049c266407c81fbad41bde1e8dfc1bb66fd267e"
        }
        response = self.client.post("/login", data=post_data, content_type="application/json")
        self.assertEqual(200, response.status_code)

    def test_login_password_error(self):
        post_data = {
            "username": "testid",
            "password": "1233"
        }
        response = self.client.post("/login", data=post_data, content_type="application/json")
        self.assertEqual(400, response.status_code)

    def test_login_not_found(self):
        post_data = {
            "username": "td",
            "password": "1233"
        }
        response = self.client.post("/login", data=post_data, content_type="application/json")
        self.assertEqual(400, response.status_code)

    def test_join_duplicate(self):
        post_data = {
            "username": "testid",
            "password": "1234",
            "personal_info": {
                "city": "北京"
            }
        }
        response = self.client.post("/join", data=post_data, content_type="application/json")
        self.assertEqual(400, response.status_code)

    def test_join_success(self):
        post_data = {
            "username": "test12",
            "password": "1234",
            "personal_info": {
                "city": "北京",
                "name": "摆烂",
                "department": "管理部门"
            }
        }
        response = self.client.post("/join", data=post_data, content_type="application/json")
        self.assertEqual(200, response.status_code)
