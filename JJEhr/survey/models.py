#-*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import DateTimeField, CharField, IntegerField, BooleanField
from django.db.models.fields.related import ForeignKey


class StaffProfile(models.Model):
    user = models.OneToOneField(User)
    division = models.CharField(max_length=30, verbose_name="所属部门")


class Survey(models.Model):
    SURVEY_TARGET = (
        ('ALL', "全体员工"),
        ('SALE', "市场营销部"),
        ("IT", "信息技术部"),
        ("CC", "呼叫中心"),
        ('F', "财务部"),
        ('P', "产品运营部")
        )
    SURVEY_STATUS = (
        ("DONE", "调查完成"),
        ("CONTINUE", "调查进行中"),
        ("EDIT", "创建问卷中"),
        ("FINISH", "问卷创建完成"),
        )

    survey_name = CharField(max_length=50, verbose_name="问卷主题", db_column="survey_name")
    survey_target = CharField(max_length=30, verbose_name="调查目标", db_column="survey_target", choices=SURVEY_TARGET)
    total_employee_number = IntegerField(verbose_name="参与调查人数", db_column="total_investigator_number")
    finish_survey_employee_number = IntegerField(verbose_name="完成调查人数",
        db_column="finish_survey_employee_number", default=0)
    survey_status = CharField(verbose_name="订单状态", max_length=30, db_column="survey_status", choices=SURVEY_STATUS, default="EDIT")

    finish_date = DateTimeField(verbose_name="调查结束时间", db_column="finish_date", null=True)
    total_page = IntegerField(db_column="total_page", default=1)

    #    model_name = CharField(max_length=30, blank=True, default=None, db_column="model_name")
    #    table_name = CharField(max_length=30, blank=True, default=None, db_column="table_name")
    create_date = DateTimeField(auto_now=True, db_column="create_date", null=True)


class SurveyItem(models.Model):
    ITEM_TYPE = (
        ('MULTIPLE_CHOICE', "复选"),
        ("SINGLE_CHOICE", "单选"),
        ('TEXT', "输入框"),
        ('TEXT_AREA', "多行输入框"),
        ('MULTIPLE_TEXT', "多行输入框"),
    )
    item_type = CharField(max_length=20, verbose_name="调查类型", choices=ITEM_TYPE, db_column="item_type")
    item_name = CharField(max_length=30, verbose_name="调查项目", db_column="item_name")
    is_required = BooleanField(verbose_name="必填", db_column="is_required")
    other_answer = BooleanField(verbose_name="是否有其他答案",db_column="other_answer")
    align_format = CharField(max_length=30,verbose_name="排列方式",db_column="align_format", null=True, blank=True)
    survey = models.ForeignKey('Survey')
    page = IntegerField(db_column="page")
    create_date = DateTimeField(auto_now=True, db_column="create_date")


class SurveyItemAnswer(models.Model):
    question_text = CharField(max_length=200, verbose_name="问题")
    question_value = CharField(max_length=200, verbose_name="问题答案")
    question_sequence = IntegerField()
    survey_item = models.ForeignKey('SurveyItem')
    create_date = DateTimeField(auto_now=True, db_column="create_date")

    class Meta:
        ordering = ['question_sequence']



class SurveyResult(models.Model):
    survey = ForeignKey(Survey)
    survey_item_name = CharField(max_length=20, verbose_name="调查项目名词", db_column="survey_item_name")
    survey_item_value = CharField(max_length=2000, verbose_name="调查结果", db_column="survey_item_value")
    survey_user = ForeignKey(User)
    create_date = DateTimeField(auto_now=True, db_column="create_date")