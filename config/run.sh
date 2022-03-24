#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python init_test.py
python manage.py runserver 0.0.0.0:80

