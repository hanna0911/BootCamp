'''
just for test: 只是用来测试前后端Login通信，后期请单独建app来写views.py（不要写在根目录里）
'''

from django.http import HttpResponse, JsonResponse

def response(code: int, data: str):
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def login(request):
    return response(200, {'success': True})