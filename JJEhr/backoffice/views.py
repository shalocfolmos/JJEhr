# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from JJEhr.lesson.models import Course



@login_required(login_url='/backoffice/login')
def test(httpRequest):
    return render_to_response('backoffice/index.html')
