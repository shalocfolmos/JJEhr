# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from JJEhr.lesson.models import Course

def test(httpRequest):
    return render_to_response('backoffice/index.html',{'course',Course.objects.get(id=1)})
