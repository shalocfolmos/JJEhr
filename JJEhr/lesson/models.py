#-*- coding: UTF-8 -*-
from django.db import models
from django import forms
from lesson.manager import CourseManager
from lesson.validation import validate_enroll

class Course(models.Model):
#    COURSE_TYPE = (
#        ('DEP', '部门培训'),
#        ('MANAGE', '管理层培训'),
#        ('FRIDAY', '周五小老师'),
#        ('EVENT', '公司活动')
#    )

    courseName = models.CharField(max_length=50)
    courseDescription = models.TextField(blank=True)
    #课时
    courseTime = models.IntegerField(blank=True)
    #课程时间安排
    courseArrange = models.CharField(max_length=100, blank=True)
    #主讲
    courseSpeaker = models.CharField(max_length=30)

    enrollStartTime = models.DateTimeField(auto_now_add=True, editable=True)
    #允许报名人数
    enrollEndTime = models.DateTimeField()

    courseStartTime = models.DateTimeField()

    maxTraineeAmount = models.IntegerField()
    courseWare = models.FileField(upload_to='courseWare_%Y_%m_%d_%M_%S', blank=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)
    #    type = models.CharField(max_length=10, choices=COURSE_TYPE)
    objects = models.Manager()
    search_objects = CourseManager()

    def __unicode__(self):
        return '(courseName = %s)' % (self.courseName,)


class Enroll(models.Model):
    email = models.EmailField()
    member_name = models.CharField(max_length=30, blank=True)
    course = models.ForeignKey('Course', db_column='courseId')
    isWaitingList = models.BooleanField(default=False)
    enrollTime = models.DateTimeField(auto_now_add=True)
    createdDate = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '(email = %s)' % (self.email,)


class EnrollForm(forms.Form):
    email = forms.EmailField(required=True, label='邮箱')
    course_id = forms.IntegerField(required=True, validators=[validate_enroll], label='课程')
