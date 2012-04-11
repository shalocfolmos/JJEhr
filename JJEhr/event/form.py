#-*- coding: UTF-8 -*-
from django.forms import forms
from JJEhr.event.models import EventType

class AddEventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
