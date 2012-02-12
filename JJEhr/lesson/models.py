#-*- coding: UTF-8 -*-
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db import models
from django import forms
from lesson.manager import CourseManager
from lesson.validation import validate_enroll

# Create your models here.
class Course(models.Model):
    courseName = models.CharField(max_length=50)
    courseDescription = models.TextField(blank=True)
    #课时
    courseTime = models.IntegerField()
    #课程时间安排
    courseArrange = models.CharField(max_length=100)
    #主讲
    courseSpeaker = models.CharField(max_length=30)

    #是否关闭
    isOpen = models.BooleanField(default=True)
    #开课时间
    startTime = models.DateTimeField(blank=False)
    #报名时间
    enterTime = models.DateTimeField(auto_now_add=True, editable=True)
    #允许报名人数
    maxTraineeAmount = models.IntegerField()
    courseWare = models.FileField(upload_to='courseWare_%Y_%m_%d_%M_%S',blank=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    search_objects = CourseManager()
    def __unicode__(self):
        return '(courseName = %s)' % (self.courseName,)

class Enroll(models.Model):
    email = models.EmailField()
    member_name = models.CharField(max_length=30,blank=True)
    course = models.ForeignKey('Course', db_column='courseId')
    enrollTime = models.DateTimeField(auto_now_add=True)
    createdDate = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '(email = %s)' % (self.email,)
class EnrollForm(forms.Form):
    email = forms.EmailField(required=True,label='邮箱')
    course_id =forms.IntegerField(required=True,validators=[validate_enroll],label='课程')
