# coding=UTF-8
import datetime
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from JJEhr import settings
from JJEhr.backoffice.form import UpdateCourseForm, AddCourseForm
from JJEhr.lesson.models import Course, Enroll
from JJEhr.backoffice.context_processor import event_type_image_prefix_url

@login_required(login_url='/backoffice/login')
def courseView(request, courseId=0):
    course = Course.objects.get(id=courseId)
    notWaitList = Enroll.objects.filter(course=course).filter(isWaitingList=False)
    waitingList = Enroll.objects.filter(course=course).filter(isWaitingList=True)

    if request.method == 'POST':
        form = UpdateCourseForm(request.POST, request.FILES)
        if form.is_valid():
            waitingList = request.POST['waitingList']
            notWaitList = request.POST['notWaitingList']
            if waitingList:
                for enrollId in waitingList.split('|'):
                    enroll = Enroll.objects.get(id=enrollId)
                    if not enroll.isWaitingList:
                        enroll.isWaitingList = True
                        enroll.save()
            if notWaitList:
                for enrollId in notWaitList.split('|'):
                    enroll = Enroll.objects.get(id=enrollId)
                    if enroll.isWaitingList:
                        enroll.isWaitingList = False
                        enroll.save()
            if request.FILES.get('courseWare'):
                course.courseWare = request.FILES.get('courseWare')
            course.save()
            return HttpResponseRedirect("/backoffice/index.html")
    else:
        form = UpdateCourseForm(instance=course)
    return render_to_response("backoffice/courseView.html",
            {"course": course, "waitingList": waitingList, "notWaitingList": notWaitList, 'form': form},
        context_instance=RequestContext(request))


@login_required(login_url='/backoffice/login')
def delete_course(request, courseId=0):
    course = Course.objects.get(id=courseId)
    if not course:
        return HttpResponseRedirect("/backoffice/index.html")
    course.delete()
    return HttpResponseRedirect("/backoffice/index.html")


@require_http_methods(["POST"])
@login_required(login_url='/backoffice/login')
def to_send_email_page(request):
    response_list = request.POST["recipient_list"].replace(u";", u"    ")
    return render_to_response("backoffice/sendEmail.html", {"recipient_list": response_list})


@require_http_methods(["POST"])
@login_required(login_url='/backoffice/login')
def send_notification_email(request):
    recipient_list = []
    for recipient in request.POST["recipient_list"].split(u"   "):
        recipient_list.append(recipient)
    send_mail(subject=request.POST["email_subject"],
        message=request.POST["email_message"],
        from_email=settings.ENROLL_EMAIL_FROM,
        recipient_list=recipient_list,
        fail_silently=False)
    return redirect("/backoffice/index.html")


@login_required(login_url='/backoffice/login')
@csrf_protect
def addCourse(request):
    if request.method == 'POST':
        courseForm = AddCourseForm(request.POST, request.FILES)
        if courseForm.is_valid():
            courseForm.save()
            return HttpResponseRedirect("/backoffice/index.html")
    else:
        courseForm = AddCourseForm(initial={'enrollStartTime': datetime.datetime.now().strftime("%Y-%m-%d")})
    return render_to_response('backoffice/courseAdd.html', {'form': courseForm},
        context_instance=RequestContext(request))


@login_required(login_url='/backoffice/login')
def displayCourseList(httpRequest):
    courseList = Course.objects.all().order_by("-updatedDate")
    request_context = RequestContext(httpRequest, {"courseList": courseList}, [event_type_image_prefix_url])
    return render_to_response("backoffice/courseList.html", {"courseList": courseList},
        context_instance=request_context)


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
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect("backoffice/index.html")
    else:
        context["exception"] = r'用户名密码不匹配'
        return HttpResponseRedirect("backoffice/login.html", context)


@login_required(login_url='/backoffice/login')
def admin_logout(request):
    return logout(request, next_page=reverse('backoffice.views.displayCourseList'))



