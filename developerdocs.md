# 这是后端开发者的文档

希望每一位后端的开发者在自己的开发过程中都能够及时维护这个文档

从配置环境开始

```shell
pip install -r requirements_dev.txt
```

以下是当前文件树(可以用tree命令来获得当前文件树)

```
.
├── Dockerfile
├── README.md
├── api  (这是未来开发API使用的app目录)
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── backend (这是总项目设置目录)
│   ├── __init__.py
│   ├── __pycache__
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── config (这里用于部署的设置)
│   ├── config.py
│   └── run.sh
├── developerdocs.md (开发者文档)
├── manage.py
├── requirements.txt (依赖文件)
├── requirements_dev.txt
├── sonar-project.properties
└── templates (模板文件夹)
```





## 注意事项

1. 项目对风格检查有严格要求, 在每次push前, 都要使用如下两个命令确定代码风格正确`pycodestyle api`, `pylint api`;其中api是项目文件夹, 在未来项目扩展时, 这些参数应当相应扩增。
2. 
