from django.db import models

# Create your models here.
class Lesson(models.Model):
    lesson_name = models.CharField(max_length=50)
    is_open = models.BooleanField()
    #开课时间
    start_time = models.DateField()
    #报名时间
    enter_time = models.DateField(auto_now_add=True)