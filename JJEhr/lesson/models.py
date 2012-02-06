#-*- coding: UTF-8 -*-
from django.db import models

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
    startTime = models.DateField(blank=False)
    #报名时间
    enterTime = models.DateField(auto_now_add=True, editable=True)
    #允许报名人数
    maxTraineeAmount = models.IntegerField()
    courseWare = models.FileField(upload_to='courseWare_%Y_%m_%d_%M_%S')
    createDate = models.DateField(auto_now_add=True)
    updatedDate = models.DateField(auto_now=True)


class Enroll(models.Model):
    email = models.EmailField()
    course = models.ForeignKey('Course',db_column='courseId')
    enrollTime = models.DateField(auto_now_add=True)
    createdDate = models.DateField(auto_now=True)
