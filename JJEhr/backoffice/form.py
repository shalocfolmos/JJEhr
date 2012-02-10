# coding=UTF-8
from django import forms

class CourseForm(forms.Form):
    courseName = forms.CharField(max_length=50)
    courseDescription = forms.Textarea()
    #课时
    courseTime = forms.IntegerField()
    #课程时间安排
    courseArrange = forms.CharField(max_length=100)
    #主讲
    courseSpeaker = forms.CharField(max_length=30)

    #是否关闭
#    isOpen = forms.BooleanField(default=True)
    #开课时间
    startTime = forms.DateTimeField()
    #报名时间
    enterTime = forms.DateTimeField()
    #允许报名人数
    maxTraineeAmount = forms.IntegerField()
    courseWare = forms.FileField()

