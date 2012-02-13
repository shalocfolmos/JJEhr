#coding=utf-8
# Create your views here.
import datetime
import os
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render_to_response,get_object_or_404
import settings
from JJEhr.lesson.models import Course, Enroll, EnrollForm
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template.context import RequestContext

def index(httpRequest):
    course_list = Course.search_objects.search( **httpRequest.GET)
    allow_course_id=[]
    allow_enroll_course_list = Course.objects.filter(enrollStartTime__lte=datetime.datetime.now()).filter(enrollEndTime__gt=datetime.datetime.now())
    for course in allow_enroll_course_list:
        allow_course_id.append(course.id)
    return render_to_response('lesson/index.html', {'course_list': course_list,'allow_course_id_list':allow_course_id},context_instance=RequestContext(httpRequest))

def detail(request, id):
    try:
        course_id = int(id)
    except ValueError:
        raise Http404
    course = get_object_or_404(Course,id=course_id)
    enroll_set = course.enroll_set.order_by('-createdDate')
    context = {'course': course,'enroll_set': enroll_set,}
    return render_to_response('lesson/show.html', context, context_instance=RequestContext(request))

#book course
def book_course(request):
    # Make sure page request is POST. If not, return Illegal.
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            _email = form._raw_value('email')
            _course = Course.objects.get(id=form._raw_value("course_id"))
            enroll_count = Enroll.objects.filter(email = _email, course = _course).count()
            if enroll_count > 0:
                return HttpResponse('You repeat reservation')
            else:
                enroll = Enroll(email=_email, course=_course)

                successEnrollMemberCount = Enroll.objects.filter(isWaitingList=False).count()
                if successEnrollMemberCount>=_course.maxTraineeAmount:
                    enroll.isWaitingList=True
                enroll.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("input Invaild")
    else:
        return HttpResponse('Illegal submit!!!')

#def search(request):
#    course_list = Course.search_objects.search( **request.GET )
#    return render_to_response('lesson/index.html', {'course_list': course_list})

def download(request):
    filename = request.GET['file']
    showName = filename.split("/")[1]
    path = settings.MEDIA_ROOT+ "/" + filename
    wrapper = FileWrapper(file(path))
    response = HttpResponse(wrapper.__getitem__(path),
        content_type='multipart/octet-stream')
    response['Content-Disposition'] = 'attachment; filename='+showName
    response['Content-Length'] = os.path.getsize(path)
    return response
