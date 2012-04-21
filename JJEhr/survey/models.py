#-*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import DateTimeField, CharField, TextField
from django.db.models.fields.related import ForeignKey


class Investigation(models.Model):
    investigation_name = CharField(max_length=50, verbose_name="调查名称", db_column="investigation_name")
    investigation_description = TextField(verbose_name="调查介绍", blank=True, db_column="investigation_description")
    investigation_source = CharField(max_length=30, verbose_name="调查目的", db_column="investigation_source")
    finish_date = DateTimeField(verbose_name="调查结束时间", db_column="finish_date")
    model_name = CharField(max_length=30, blank=True, default=None, db_column="model_name")
    table_name = CharField(max_length=30, blank=True, default=None, db_column="table_name")
    create_date = DateTimeField(auto_now=True, db_column="create_date")


class InvestigationItem(models.Model):
    ITEM_TYPE = (
        ('MULTIPLE', "复选"),
        ("SINGLE", "单选"),
        ('DESCRIPTION', "介绍")
        )
    item_type = CharField(max_length=20, verbose_name="调查类型", choices=ITEM_TYPE, db_column="item_type")
    item_name = CharField(max_length=30, verbose_name="调查项目", db_column="item_name")
    item_default_value = CharField(max_length=30, verbose_name="默认值", db_column="item_default_value")
    investigation = ForeignKey(Investigation)
    create_date = DateTimeField(auto_now=True, db_column="create_date")


class InvestigationResult(models.Model):
    investigation = ForeignKey(Investigation)
    investigation_item_name = CharField(max_length=20, verbose_name="调查项目名词", db_column="investigation_item_name")
    investigation_item_value = CharField(max_length=2000, verbose_name="调查结果", db_column="investigation_item_value")
    investigation_user = ForeignKey(User)
    create_date = DateTimeField(auto_now=True, db_column="create_date")