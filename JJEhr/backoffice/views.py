# coding=UTF-8
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from JJEhr.backoffice.form import CourseForm
from JJEhr.lesson.models import Course
from django.contrib.sites.models import get_current_site



@login_required(login_url='/backoffice/login')
def test(httpRequest):
    return render_to_response('backoffice/index.html')

def courseView(httpRequest,courseId=0):
    course=Course.objects.get(id=courseId)
    enrollList = course.enroll_set.order_by("enrollTime")
    if enrollList:
        waitingList = enrollList[0:course.maxTraineeAmount-1]
    return render_to_response("backoffice/courseView.html",{"course":course,"waiting":waitingList})

def addCourse(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = CourseForm(request)
    return render_to_response('backoffice/courseAdd.html',{'form':form})


@login_required(login_url='/backoffice/login')
def displayCourseList(httpRequest):
    courseList = Course.objects.all().order_by("-startTime")
    return render_to_response("backoffice/courseList.html",{"courseList":courseList})

def login(request):
    currentSite = get_current_site(request)
    next = request.POST["next"]
    form = AuthenticationForm(request.POST)
    context = {
        'form': form,
        'next': next,
        'site': currentSite,
        'site_name': current_site.name,
        }
    if not form.is_valid():

        return render_to_response("/backoffice/login", context,
            context_instance=RequestContext(request, current_app=None))

    username = request.POST["username"]
    password = request.POST["passoword"]
    next = request.POST["next"]
    user = authenticate(username=username,password=password)
    if user is not None and user.is_active:
        login(request,user)
        return HttpResponseRedirect("backoffice/index.html")
    else:
        context["exception"]=r'用户名密码不匹配'
        return HttpResponseRedirect("backoffice/login.html",context)


