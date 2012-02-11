# coding=UTF-8
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from JJEhr.backoffice.form import CourseForm
from JJEhr.lesson.models import Course, Enroll
from django.contrib.sites.models import get_current_site


@login_required(login_url='/backoffice/login')
def courseView(request,courseId=0):
    course=Course.objects.get(id=courseId)
    waitingList=notWaitList=None
    notWaitList = Enroll.objects.filter(course=course).filter(isWaitingList=False)
    waitingList = Enroll.objects.filter(course=course).filter(isWaitingList=True)

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course.courseName=request.POST["courseName"]
            course.courseDescription=request.POST['courseDescription']
            course.courseTime=request.POST['courseTime']
            course.courseArrange=request.POST['courseArrange']
            course.courseSpeaker=request.POST['courseSpeaker']
            course.enterTime=request.POST['enterTime']
            course.maxTraineeAmount=request.POST['maxTraineeAmount']
            course.save()
            return HttpResponseRedirect("/backoffice/index.html")
    else:
        courseData = {
            'courseName':course.courseName,
            'courseDescription':course.courseDescription,
            'courseTime':course.courseTime,
            'courseArrange':course.courseArrange,
            'courseSpeaker':course.courseSpeaker,
            'enterTime':course.enterTime,
            'maxTraineeAmount':course.maxTraineeAmount
        }
        form = CourseForm(courseData)
    return render_to_response("backoffice/courseView.html",{"course":course,"waitingList":waitingList,"notWaitingList":notWaitList,'form':form},context_instance=RequestContext(request))

@login_required(login_url='/backoffice/login')
@csrf_protect
def addCourse(request):
    if request.method == 'POST':

        form = CourseForm(request.POST)
        if form.is_valid():
           course = Course()
           course.courseName=request.POST["courseName"]
           course.courseDescription=request.POST['courseDescription']
           course.courseTime=request.POST['courseTime']
           course.courseArrange=request.POST['courseArrange']
           course.courseSpeaker=request.POST['courseSpeaker']
           course.enterTime=request.POST['enterTime']
           course.maxTraineeAmount=request.POST['maxTraineeAmount']
           course.save()

           return HttpResponseRedirect("/backoffice/index.html")
    else:
        form = CourseForm()
    return render_to_response('backoffice/courseAdd.html',{'form':form},context_instance=RequestContext(request))


@login_required(login_url='/backoffice/login')
def displayCourseList(httpRequest):
    courseList = Course.objects.all().order_by("-updatedDate")
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


