# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import uuid

from flask_login import UserMixin

from apps import db, login_manager


def default_uuid():
    return str(uuid.uuid4())


class Student(db.Model, UserMixin):

    __tablename__ = 'student'

    id = db.Column(db.String(100), primary_key=True, default=default_uuid)
    code = db.Column(db.String(64), unique=True)
    avatar = db.Column(db.String(250))
    name = db.Column(db.String(250))
    address = db.Column(db.String(250))
    gender = db.Column(db.String())
    birthday = db.Column(db.DateTime())
    phone_number = db.Column(db.String(100))
    email = db.Column(db.String(100))
    identification = db.Column(db.String(100))  # Căn cước công dân
    health_insurance = db.Column(db.String(100))  # Bảo hiểm y tế
    student_class = db.Column(db.String(100))
    student_major = db.Column(db.String(100))
    deleted = db.Column(db.Boolean(), default=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.code)


@login_manager.user_loader
def user_loader(id):
    return Student.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    code = request.form.get('code')
    record_student = Student.query.filter_by(code=code).first()
    return record_student if record_student else None
