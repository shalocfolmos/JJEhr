# coding=UTF-8
import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from JJEhr.backoffice.form import CourseForm, UpdateCourseForm
from JJEhr.lesson.models import Course, Enroll
from django.contrib.sites.models import get_current_site


def saveUploadFile(uploadedFile):
    pass


@login_required(login_url='/backoffice/login')
def courseView(request,courseId=0):
    """

    """
    course=Course.objects.get(id=courseId)
    waitingList=notWaitList=None
    notWaitList = Enroll.objects.filter(course=course).filter(isWaitingList=False)
    waitingList = Enroll.objects.filter(course=course).filter(isWaitingList=True)

    if request.method == 'POST':
        form = UpdateCourseForm(request.POST,request.FILES)
        if form.is_valid():
            waitingList = request.POST['waitingList']
            notWaitList = request.POST['notWaitingList']
            if waitingList:
                for enrollId in waitingList.split('|'):
                    enroll = Enroll.objects.get(id=enrollId)
                    if(enroll.isWaitingList!=True):
                        enroll.isWaitingList=True
                        enroll.save()
            if notWaitList:
                for enrollId in notWaitList.split('|'):
                    enroll = Enroll.objects.get(id=enrollId)
                    if enroll.isWaitingList!=False:
                        enroll.isWaitingList=False
                        enroll.save()

            course.courseName=request.POST["courseName"]
            course.courseDescription=request.POST['courseDescription']
            course.courseTime=request.POST['courseTime']
            course.courseArrange=request.POST['courseArrange']
            course.courseSpeaker=request.POST['courseSpeaker']
            course.enrollStartTime=request.POST['enrollStartTime']
            course.enrollEndTime=request.POST['enrollEndTime']
            if request.FILES.get('courseWare'):
                course.courseWare=request.FILES.get('courseWare')
            course.save()
            return HttpResponseRedirect("/backoffice/index.html")
    else:
        courseData = {
            'courseName':course.courseName,
            'courseDescription':course.courseDescription,
            'courseTime':course.courseTime,
            'courseArrange':course.courseArrange,
            'courseSpeaker':course.courseSpeaker,
            'enrollStartTime':course.enrollStartTime,
            'enrollEndTime':course.enrollEndTime,
            'maxTraineeAmount':course.maxTraineeAmount,
            'courseWare':course.courseWare
        }
        form = UpdateCourseForm(courseData)
    return render_to_response("backoffice/courseView.html",{"course":course,"waitingList":waitingList,"notWaitingList":notWaitList,'form':form},context_instance=RequestContext(request))

@login_required(login_url='/backoffice/login')
def delete_course(request,courseId=0):
    course=Course.objects.get(id=courseId)
    if not course:
        return HttpResponseRedirect("/backoffice/index.html")
    course.delete()
    return HttpResponseRedirect("/backoffice/index.html")


@login_required(login_url='/backoffice/login')
@csrf_protect
def addCourse(request):
    if request.method == 'POST':
        form = CourseForm(request.POST,request.FILES)
        if form.is_valid():
           course = Course()
           course.courseName=request.POST["courseName"]
           course.courseDescription=request.POST['courseDescription']
           course.courseTime=request.POST['courseTime']
           course.courseArrange=request.POST['courseArrange']
           course.courseSpeaker=request.POST['courseSpeaker']
           course.enrollStartTime=request.POST['enrollStartTime']
           course.enrollEndTime=request.POST['enrollEndTime']
           course.maxTraineeAmount=request.POST['maxTraineeAmount']
           course.courseWare=request.FILES.get('courseWare')
           course.save()
           return HttpResponseRedirect("/backoffice/index.html")
    else:
        form = CourseForm(initial={'enrollStartTime':datetime.datetime.now().strftime("%Y-%m-%d")})
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

@login_required(login_url='/backoffice/login')
def admin_logout(request):
    return logout(request,next_page=reverse('backoffice.views.displayCourseList'))
