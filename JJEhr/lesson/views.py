#coding=utf-8
# Create your views here.
import datetime
import os
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render_to_response,get_object_or_404
from lesson.manager import tempMapping
import settings
from JJEhr.lesson.models import Course, Enroll, EnrollForm

from django.http import HttpResponse
from django.template.context import RequestContext

def index(httpRequest):
    kwargs = httpRequest.GET
    isSearch = False
    if kwargs.has_key('searchType') and kwargs.has_key('searchContent') :
        current_search_type = tempMapping().getSearchType(kwargs.get('searchType'))
        searchContent = kwargs.get('searchContent')
        isSearch = True
    course_set = Course.search_objects.search(** kwargs)
    allow_course_id=[]
    for course in course_set.object_list:
        if course.enrollStartTime < datetime.datetime.now() and course.enrollEndTime > datetime.datetime.now() :
            allow_course_id.append(course.id)
    _context = {
        'course_list' :course_set,
        'allow_course_id_list':allow_course_id,
        'search_type':tempMapping().getAllSearchType(),
        'isSearch' : isSearch,
    }
    if isSearch:
        _context['current_search_type'] = current_search_type
        _context['searchContent'] = searchContent
    return render_to_response('lesson/index1.html', _context ,context_instance=RequestContext(httpRequest))

#def detail(request, id):
#    try:
#        course_id = int(id)
#    except ValueError:
#        raise Http404
#    course = get_object_or_404(Course,id=course_id)
#    enroll_set = course.enroll_set.order_by('-createdDate')
#    context = {'course': course,'enroll_set': enroll_set,}
#    return render_to_response('lesson/show.html', context, context_instance=RequestContext(request))

##  Illegal submit ->403
##  input Invaild not email  ->  400
##  repeat reservation 409
## success 200
## date time 404
#book course
def book_course(request):
    # Make sure page request is POST. If not, return Illegal.
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            _email = form._raw_value('email')
            _course = Course.objects.get(id=form._raw_value("course_id"))
            if _course.enrollStartTime > datetime.datetime.now() or _course.enrollEndTime < datetime.datetime.now() :
                return HttpResponse(404)
            enroll_count = Enroll.objects.filter(email = _email, course = _course).count()
            if enroll_count > 0:
                return HttpResponse(409)
            else:
                enroll = Enroll(email=_email, course=_course)
                successEnrollMemberCount = Enroll.objects.filter(isWaitingList=False).count()
                if successEnrollMemberCount>=_course.maxTraineeAmount:
                    enroll.isWaitingList=True
                enroll.save()
            return HttpResponse(200)
        else:
            return HttpResponse(400)
    else:
        return HttpResponse(403)

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
