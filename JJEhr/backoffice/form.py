# coding=UTF-8
from django.db.models.fields import TextField
from django.forms.fields import   CharField
from django.forms.forms import Form
from django.forms.models import ModelForm
from JJEhr.lesson.models import Course

class AddCourseForm(ModelForm):
    class Meta:
        model = Course


class UpdateCourseForm(ModelForm):
    class Meta:
        model = Course


class ExportContactsForm(Form):
    recipient_list = CharField()


class SendEmailForm(Form):
    recipient_list = CharField()
    head = CharField(label="邮件主题")
    message = TextField(label="邮件内容")
