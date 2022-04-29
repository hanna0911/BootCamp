"""
描述数据库结构的文件
"""
import datetime
from email.policy import default
from random import choice
from django.db import models

# Create your models here.

NAME_LEN = 50
SHORT_INFO_LEN = 20
LONG_INFO_LEN = 200
COMMENT_LEN = 500
JoinStatusToText = ["待入职","在职","离职"]
EmployeeTypeToText = ["校招","社招","实习","未选择"]
GraduateStatusToTest = ["未毕业","正常毕业","非正常毕业"]
TeacherExaminedStatusToTest = ["未审核","审核通过","审核拒绝"]
HonorToTest = ["奖章","证书","奖项"]


class PrivateInfo(models.Model):
    """
    user table
    """

    # --------------------Enum枚举类的实现--------------------
    class EnumJoinStatus(models.IntegerChoices):
        NotJoin = 0     # 待入职
        OnJob = 1       # 在职
        Dimission = 2   # 离职

    class EnumEmployeeType(models.IntegerChoices):
        Campus = 0      # 校招
        Social = 1      # 社招
        Intern = 2      # 实习
        Other = 3       # 未选择

    class EnumNewcomerGraduateState(models.IntegerChoices):
        NotGraduate = 0         # 未毕业
        NormalGraduate = 1      # 正常毕业
        AbnormalGraduate = 2    # 非正常毕业

    class EnumTeacherExaminedStatus(models.IntegerChoices):
        NotYet = 0  # 未审核
        Pass = 1  # 审核通过
        Fail = 2  # 审核拒绝
    # --------------------------------------------------------

    username = models.CharField(max_length=NAME_LEN)  # 用户用于登录的用户名
    password = models.CharField(max_length=LONG_INFO_LEN)  # 用户密码(加密后)

    name = models.CharField(max_length=NAME_LEN)  # 用户的真实姓名
    city = models.CharField(max_length=SHORT_INFO_LEN)  # 用户所在城市
    dept = models.CharField(max_length=SHORT_INFO_LEN)  # 用户所在部门
    avatar = models.ImageField()  # 用户头像
    bio = models.CharField(max_length=LONG_INFO_LEN)  # 签名

    joinDate = models.DateTimeField(null=True)  # 用户入职时间
    joinStatus = models.IntegerField(choices = EnumJoinStatus.choices, default = EnumJoinStatus.NotJoin)  # 入职情况,0代表待入职,1代表在职,2代表离职
    detail = models.CharField(max_length=1000)  # 详细信息
    leader = models.CharField(max_length=NAME_LEN)  # 直属上级
    registrationDate = models.DateTimeField(auto_now_add=True)  # 注册时间
    employeeType = models.IntegerField(choices = EnumEmployeeType.choices, default = EnumEmployeeType.Other)  # 员工类型，例如长期工、实习工等

    # 用户身份相关
    isAdmin = models.BooleanField(default=False)  # 是否是管理员
    isTeacher = models.BooleanField(default=False)  # 是否是老师
    isHRBP = models.BooleanField(default=False)  # 是否是HRBP
    isNew = models.BooleanField(default=False)  # 是否是新人

    # 新人相关
    newcomerStartDate = models.DateTimeField(null=True)  # 新人旅程开始时间，是用户isNew被设为True的时间
    newcomerGraduateState = models.IntegerField(choices = EnumNewcomerGraduateState.choices, default = EnumNewcomerGraduateState.NotGraduate)  # 新人是否已经毕业
    newcomerGraduateDate = models.DateTimeField(null=True)  # 新人毕业时间

    # 导师相关
    historicalMembers = models.IntegerField(default=0)  # 历史带新人数
    currentMembers = models.IntegerField(default=0)  # 当前带新人数
    teacherNominationDate = models.DateTimeField(null=True)  # 导师被提名时间，也是导师旅程开始时间，是用户isTeacher被设为True的时间
    teacherExaminedStatus = models.IntegerField(
        choices = EnumTeacherExaminedStatus.choices,
        default = EnumTeacherExaminedStatus.NotYet)  # 审核状态，默认值为“未审核”。使用Django枚举类型实现
    teacherExaminedDate = models.DateTimeField(null=True)  # 导师被hrbp审核通过时间
    teacherIsDuty = models.BooleanField(default=False)  # 导师是否上岗
    teacherDutyDate = models.DateTimeField(null=True)  # 导师上岗时间
    teacherScore = models.FloatField(default=0)  # 老师被新人评价的平均分数


class Honor(models.Model):
    """
    个人荣誉
    """

    # --------------------Enum枚举类的实现--------------------
    class EnumType(models.IntegerChoices):
        Medal = 0           # 勋章
        Certificate = 1     # 证书
        Award = 2           # 奖项
    # --------------------------------------------------------

    type = models.IntegerField(choices = EnumType.choices, default = EnumType.Medal)  # Honor类型，默认为“勋章”
    owner = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE)  # 荣誉的归属者
    text = models.CharField(max_length=LONG_INFO_LEN, default="None")  # 奖励描述
    pic = models.ImageField()  # 荣誉图片


class TeacherNewcomerTable(models.Model):
    """
    描述导师和新人间关系的表
    """
    relationID = models.AutoField(primary_key=True)  # 自增主键
    teacher = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE, related_name="AsTeacher")  # 外键，该关系中的导师
    newcomer = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE, related_name="AsNewcomer")  # 外键，该关系中的新人
    teacherScore = models.FloatField(default=-1.)  # 该老师被该新人评价的分数
    newcomerToTeacher = models.CharField(max_length=COMMENT_LEN)  # 该新人对该导师的评语
    newcomerScore = models.FloatField(default=-1.)  # 该新人被该老师评价的分数
    teacherToNewcomer = models.CharField(max_length=COMMENT_LEN)  # 该导师对该新人的评语


class NewcomerRecode(models.Model):
    """
    导师对新人的带新记录
    """
    content = models.CharField(max_length=COMMENT_LEN)
    teacher = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE, related_name="RecodeTeacher")  # 外键，该关系中的导师
    newcomer = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE, related_name="RecodeNewcomer")  # 外键，该关系中的新人
    commitTime = models.DateTimeField(auto_now_add=True)  # 带新记录发表的时间


class ProgramTable(models.Model):
    """
    大的培训项目的表
    """

    # --------------------Enum枚举类的实现--------------------
    class EnumAudience(models.IntegerChoices):
        Newcomer = 0    # 新人
        Teacher = 1     # 老师
    # --------------------------------------------------------

    id = models.CharField(primary_key=True, max_length=NAME_LEN)  # 项目id
    name = models.CharField(max_length=NAME_LEN)  # 项目名称
    author = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE)  # 项目作者或者管理者
    intro = models.CharField(max_length=LONG_INFO_LEN)  # 项目简介
    tag = models.CharField(max_length=LONG_INFO_LEN)  # 项目标签
    contentCount = models.IntegerField()  # 子项目数
    recommendTime = models.IntegerField(null=True)  # 推荐（默认）完成时间，用于生成默认ddl
    audience = models.IntegerField(choices = EnumAudience.choices)  # 项目受众，无默认值
    cover = models.ImageField()  # 项目封面
    releaseTime = models.DateTimeField(auto_now_add=True)  # 发布时间


class ContentTable(models.Model):
    """
    包括course exam task
    """

    # --------------------Enum枚举类的实现--------------------

    class EnumType(models.IntegerChoices):
        Course = 0  # course
        Exam = 1    # exam
        Task = 2    # task

    class EnumTaskType(models.IntegerChoices):
        Text = 0    # text
        Link = 1    # link
        File = 2    # file
    # --------------------------------------------------------

    id = models.CharField(primary_key=True, max_length=NAME_LEN)  # 事件id
    name = models.CharField(max_length=NAME_LEN)  # 事件名称
    author = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE, blank=True)  # 事件作者
    intro = models.CharField(max_length=LONG_INFO_LEN)  # 事件简介
    tag = models.CharField(max_length=LONG_INFO_LEN)  # 事件标签
    recommendedTime = models.IntegerField()  # 建议用时，若为考试则为考试限时
    audience = models.IntegerField()  # 受众
    cover = models.ImageField()  # 封面
    type = models.IntegerField(choices = EnumType.choices)  # content类型 0 代表course，1代表exam，2代表task
    isTemplate = models.BooleanField()  # 是否是模板
    programId = models.ForeignKey(ProgramTable, on_delete=models.CASCADE)  # 所属的Programid
    releaseTime = models.DateTimeField(auto_now_add=True)  # 发布时间
    # course相关
    lessonCount = models.IntegerField()  # lesson数
    # exam相关
    questions = models.CharField(max_length=1000)  # 考题csv的地址
    beginTime = models.DateTimeField(null=True)  # 官方提供的开始时间
    endTime = models.DateTimeField(null=True)  # 官方提供的结束时间
    # task相关
    taskType = models.IntegerField(choices = EnumTaskType.choices, default = EnumTaskType.Text)  # 任务类型(针对task类 0-text, 1-link, 2-file)
    text = models.CharField(max_length=10000)  # 任务文字(针对task类)
    link = models.URLField(max_length=LONG_INFO_LEN)  # 任务链接
    taskFile = models.CharField(max_length=1000)  # 任务文件


class LessonTable(models.Model):
    """
    课程库,隶属于培训内容库
    """
    id = models.CharField(primary_key=True, max_length=NAME_LEN)  # 课堂id
    name = models.CharField(max_length=NAME_LEN)  # 课堂名称
    author = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE, blank=True)  # 课堂作者
    content = models.ForeignKey(ContentTable, on_delete=models.CASCADE)  # 课堂所属的事件或者大课程
    intro = models.CharField(max_length=LONG_INFO_LEN)  # 课堂介绍
    recommendedTime = models.IntegerField()  # 建议用时
    cover = models.ImageField()  # 封面
    releaseTime = models.DateTimeField(auto_now_add=True)  # 发布时间


class CoursewareTable(models.Model):
    """
    课件库
    """
    id = models.CharField(primary_key=True, max_length=NAME_LEN)  # 课件id
    lesson = models.ForeignKey(LessonTable, on_delete=models.CASCADE)  # 所属课堂
    content = models.ForeignKey(ContentTable, on_delete=models.CASCADE)  # 所属课程或事件
    name = models.CharField(max_length=NAME_LEN)  # 名称
    cover = models.ImageField()  # 封面
    uploadTime = models.DateTimeField(auto_now_add=True)  # 上传时间
    url = models.CharField(max_length=LONG_INFO_LEN)  # 课件地址


class ProgramContentTable(models.Model):
    """
    Program-Content对照表（考虑到不同Program可能共用一个Content）
    """
    relationID = models.AutoField(primary_key=True)  # 自增主键
    program = models.ForeignKey(ProgramTable, on_delete=models.CASCADE)  # Program
    content = models.ForeignKey(ContentTable, on_delete=models.CASCADE)  # 属于这个Program的Content


class UserProgramTable(models.Model):
    """
    用户-Program（一个Program是若干课程、任务和考试打成的包）关系表
    """
    relationID = models.AutoField(primary_key=True)  # 自增主键
    user = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE, related_name="ProgramsAsUser")  # 本记录所属用户
    program = models.ForeignKey(ProgramTable, on_delete=models.CASCADE)  # 本记录所属Program
    finishedContentCount = models.IntegerField(default=0)  # 完成的内容数
    finished = models.BooleanField(default=False)  # 是否完成
    beginTime = models.DateTimeField(auto_now_add=True)  # 开始时间
    endTime = models.DateTimeField(null=True)  # 结束时间（仅结束后有意义，完成项目时赋值）
    deadline = models.DateTimeField(null=True)  # 项目对于个人来说的ddl
    assigner = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE, related_name="ProgramsAsAssigner")  # 该program的指派人
    score = models.IntegerField(default=-1)  # 分数（考试分数取加权平均，没有考试则数据无效）


class UserContentTable(models.Model):
    """
    用户-培训内容（包括单个课程、任务和考试）关系表
    """
    relationID = models.AutoField(primary_key=True)  # 自增主键
    user = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE, related_name="ContentAsUser")  # 用户
    content = models.ForeignKey(ContentTable, on_delete=models.CASCADE)  # 培训内容
    finished = models.BooleanField(default=False)  # 是否结束
    userBeginTime = models.DateTimeField(auto_now_add=True)  # 开始时间 这个时间属于个人
    userEndTime = models.DateTimeField(default=datetime.datetime.fromisoformat("2000-01-01 00:00"))  # 结束时间  这个时间属于个人
    deadline = models.DateTimeField()  # 单个培训内容对个人来说的ddl
    assigner = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE, related_name="ContentAsAssigner")  # 该content的指派人

    # course相关
    isObligatory = models.BooleanField(default=True)  # 课程是否是必修
    finishedLessonCount = models.IntegerField(default=0)  # 结束的lesson数量

    # exam相关
    examUsedTime = models.IntegerField(default=-1)  # 个人考试用时
    score = models.IntegerField(default=-1)  # 分数（仅对考试类型的Content有效）

    # task相关


class UserLessonTable(models.Model):
    """
    用户-课程Lesson（Lesson是Course的子项）
    """
    relationID = models.AutoField(primary_key=True)  # 自增主键
    user = models.ForeignKey(PrivateInfo, on_delete=models.CASCADE)  # 用户
    lesson = models.ForeignKey(LessonTable, on_delete=models.CASCADE)  # 课程
    finished = models.BooleanField(default=False)  # 是否结束
    beginTime = models.DateTimeField(auto_now_add=True)  # 开始时间
    endTime = models.DateTimeField()  # 结束时间
