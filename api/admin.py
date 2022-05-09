"""
注册模型用
"""
from api.models import PrivateInfo, ProgramTable, UserProgramTable, UserContentTable, ContentTable, ProgramContentTable
from django.contrib import admin

# Register your models here.
admin.site.register(PrivateInfo)
admin.site.register(ProgramTable)
admin.site.register(UserProgramTable)
admin.site.register(UserContentTable)
admin.site.register(ContentTable)
admin.site.register(ProgramContentTable)
