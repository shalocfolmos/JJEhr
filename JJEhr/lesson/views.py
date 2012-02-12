#coding=utf-8
# Create your views here.
from django.shortcuts import render_to_response,get_object_or_404
from JJEhr.lesson.models import Course, Enroll, EnrollForm
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template.context import RequestContext

def index(httpRequest):
    course_list = Course.search_objects.search( **httpRequest.GET)
    return render_to_response('lesson/index1.html', {'course_list': course_list})

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
            _course = Course(id=form._raw_value("course_id"))
            enroll_count = Enroll.objects.filter(email = _email, course = _course).count()
            if enroll_count > 1:
                return HttpResponse('You repeat reservation')
            else:
                enroll = Enroll(email=_email, course=_course)
                enroll.save()
            return HttpResponseRedirect('/' + _course.id)
        else:
            return HttpResponse("input Invaild")
    else:
        return HttpResponse('Illegal submit!!!')
def search(request):
    course_list = Course.search_objects.search( **request.GET )
    return render_to_response('lesson/index.html', {'course_list': course_list})
