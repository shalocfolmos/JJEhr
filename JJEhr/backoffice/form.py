# coding=UTF-8
from django.forms.fields import DateTimeField, FileField, CharField, IntegerField
from django.forms.forms import Form
from django.forms.models import ModelForm
from django.forms.widgets import DateInput, Textarea
from JJEhr.lesson.models import Course

class AddCourseForm(ModelForm):
    class Meta:
        model = Course


class UpdateCourseForm(Form):
    courseName = CharField(max_length=50, label="课程名称")

    courseDescription = CharField(label="课程介绍： ", widget=Textarea)
    #主讲
    courseSpeaker = CharField(max_length=30, label="主讲人 ")
    #课时
    courseTime = IntegerField(required=False, label="课时")
    courseStartTime = DateTimeField(label="开始上课日期", widget=DateInput(format="%Y-%m-%d"), required=True)
    courseArrange = CharField(max_length=100, required=False, label="课程安排 ")

    enrollStartTime = DateTimeField(label="报名开始时间", widget=DateInput(format='%Y-%m-%d'), required=True)

    enrollEndTime = DateTimeField(label="报名结束时间", widget=DateInput(format='%Y-%m-%d'), required=True)
    courseWare = FileField(required=False, label="课件")


class ExportContactsForm(Form):
    recipient_list = CharField()