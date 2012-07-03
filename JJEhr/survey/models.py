#-*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import DateTimeField, CharField, IntegerField, BooleanField
from django.db.models.fields.related import ForeignKey


class Investigation(models.Model):
    ITEM_TYPE = (
        ('SALES_DEPARTMENT', "复选"),
        ("INFORMATION_DEPARTMENT", "信息技术部"),
        ("CALL_CENTER_DEPARTMENT", "呼叫中心"),
        ('FINANCE_DEPARTMENT', "财务部")
        )

    investigation_name = CharField(max_length=50, verbose_name="问卷主题", db_column="investigation_name")
    investigation_target = CharField(max_length=30, verbose_name="调查目标", db_column="investigation_target")
    total_employee_number = IntegerField(verbose_name="参与调查人数", db_column="total_investigator_number")
    finish_investigation_employee_number = IntegerField(verbose_name="完成调查人数",
        db_column="finish_investigation_employee_number", default="0")
    investigation_status = IntegerField(verbose_name="订单状态", db_column="investigation_status")

    finish_date = DateTimeField(verbose_name="调查结束时间", db_column="finish_date", null=True)
    total_page = IntegerField(db_column="total_page", default=1)

    #    model_name = CharField(max_length=30, blank=True, default=None, db_column="model_name")
    #    table_name = CharField(max_length=30, blank=True, default=None, db_column="table_name")
    create_date = DateTimeField(auto_now=True, db_column="create_date")


class InvestigationItem(models.Model):
    ITEM_TYPE = (
        ('MULTIPLE', "复选"),
        ("SINGLE", "单选"),
        ('DESCRIPTION', "介绍")
        )
    item_type = CharField(max_length=20, verbose_name="调查类型", choices=ITEM_TYPE, db_column="item_type")
    item_name = CharField(max_length=30, verbose_name="调查项目", db_column="item_name")
    is_optional_answer = BooleanField(verbose_name="可选答案", db_column="is_optional_answer")
    item = models.ForeignKey('Investigation')
    page = IntegerField(db_column="page")

    create_date = DateTimeField(auto_now=True, db_column="create_date")


class InvestigationItemAnswer(models.Model):
    question_title = CharField(max_length=100, verbose_name="问题")
    question_sequence = IntegerField()
    investigation_item = models.ForeignKey('InvestigationItem')
    create_date = DateTimeField(auto_now=True, db_column="create_date")


class InvestigationResult(models.Model):
    investigation = ForeignKey(Investigation)
    investigation_item_name = CharField(max_length=20, verbose_name="调查项目名词", db_column="investigation_item_name")
    investigation_item_value = CharField(max_length=2000, verbose_name="调查结果", db_column="investigation_item_value")
    investigation_user = ForeignKey(User)
    create_date = DateTimeField(auto_now=True, db_column="create_date")