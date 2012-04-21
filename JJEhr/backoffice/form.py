# coding=UTF-8
from django.forms.fields import   CharField, SlugField
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
    head = CharField(label=u"邮件主题")
    message = SlugField(label=u"邮件内容")
