#-*- coding: UTF-8 -*-
from django.forms.fields import EmailField, IntegerField
from django.forms.forms import Form
from lesson.validation import validate_enroll

class EnrollForm(Form):
    email = EmailField(required=True, label='邮箱')
    course_id = IntegerField(required=True, validators=[validate_enroll], label='课程')
