#-*- coding: UTF-8 -*-
import datetime
from django.shortcuts import render_to_response
from lesson.manager import tempMapping
import settings
from JJEhr.lesson.form import EnrollForm
from JJEhr.lesson.models import Course, Enroll

from django.http import HttpResponse
from django.template.context import RequestContext

def index(httpRequest):
    kwargs = httpRequest.GET
    isSearch = False
    if kwargs.has_key('searchType') and kwargs.has_key('searchContent'):
        current_search_type = tempMapping().getSearchType(kwargs.get('searchType'))
        searchContent = kwargs.get('searchContent')
        isSearch = True
    course_set = Course.search_objects.search(**kwargs)
    allow_course_id = []
    for course in course_set.object_list:
        if course.enrollStartTime < datetime.datetime.now() and course.enrollEndTime > datetime.datetime.now():
            allow_course_id.append(course.id)
    _context = {
        'course_list': course_set,
        'allow_course_id_list': allow_course_id,
        'search_type': tempMapping().getAllSearchType(),
        'isSearch': isSearch,
        }
    if isSearch:
        _context['current_search_type'] = current_search_type
        _context['searchContent'] = searchContent
    return render_to_response('lesson/index.html', _context, context_instance=RequestContext(httpRequest))


def book_course(request):
    # Make sure page request is POST. If not, return Illegal.
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            _email = form._raw_value('email')
            _course = Course.objects.get(id=form._raw_value("course_id"))
            if _course.enrollStartTime > datetime.datetime.now() or _course.enrollEndTime < datetime.datetime.now():
                return HttpResponse(404)
            enroll_count = Enroll.objects.filter(email=_email, course=_course).count()
            if enroll_count > 0:
                return HttpResponse(409)
            else:
                enroll = Enroll(email=_email, course=_course)
                successEnrollMemberCount = Enroll.objects.filter(isWaitingList=False).count()
                if successEnrollMemberCount > _course.maxTraineeAmount:
                    enroll.isWaitingList = True
                enroll.save()
            return HttpResponse(200)
        else:
            return HttpResponse(400)
    else:
        return HttpResponse(403)
