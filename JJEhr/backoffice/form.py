# coding=UTF-8
from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms.widgets import DateTimeInput, DateInput
from JJEhr.lesson.models import Course

class CourseForm(forms.Form):
    class Meta:
        model = Course

    courseName = forms.CharField(max_length=50,label="课程名称: ")

    courseDescription = forms.CharField(label="课程介绍： ",widget=forms.Textarea)
    #课时
    courseTime = forms.IntegerField(required=False,label="课时： ")
    #课程时间安排
    courseArrange = forms.CharField(max_length=100,required=False,label="课程安排： ")
    #主讲
    courseSpeaker = forms.CharField(max_length=30,label="主讲人 ")

    #是否关闭
#    isOpen = forms.BooleanField(default=True)
    #报名时间
    enterTime = forms.DateTimeField(label="报名时间：", widget=DateInput(format='%Y-%m-%d'))
    #允许报名人数
    maxTraineeAmount = forms.IntegerField(label="最大报名人数：")
    courseWare = forms.FileField(required=False,label="课时：")

