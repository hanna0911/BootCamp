"""
暂行的一部分接口文件,之后开始写接口后按接口分类进行文件划分
"""
# from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import User


# Create your views here.

def test(request: HttpRequest):
    """
    for test
    :param request:
    :return:
    """
    if request.method == "GET":
        print("hello")
    user = User(name="hello")
    user.save()
    out = User.objects.all().first()
    return HttpResponse("ok,"+out.name)
