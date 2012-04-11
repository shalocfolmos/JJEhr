#-*- coding: UTF-8 -*-
from django.forms.models import ModelForm

from JJEhr.event.models import EventType

class AddEventTypeForm(ModelForm):
    class Meta:
        model = EventType
