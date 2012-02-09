# Create your views here.
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from JJEhr.lesson.models import Course, Enroll, EnrollForm
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponse

def index(httpRequest):
    # default show 20 courses per page
    page_size = 2
    course_list = Course.objects.order_by("-createDate")
    paginator = Paginator(course_list, page_size)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(httpRequest.GET.get('page', "1"))
    except ValueError:
        page = 1
        # If page request (9999) is out of range, deliver last page of results.
    try:
        course_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        course_list = paginator.page(paginator.num_pages)

    return render_to_response('lesson/index.html', {'course_list': course_list})


def detail(request, id):
    try:
        course_id = int(id)
    except ValueError:
        raise Http404
    try:
        course = Course.objects.get(id=course_id)
    except (Course.DoesNotExist):
        raise Http404
    enroll_set = course.enroll_set.order_by('-createdDate')
    context = {'course': course,
               'enroll_set': enroll_set,
               }
    return render_to_response('lesson/show.html', context,context_instance=RequestContext(request))

#book course

def book_course(request):
    # Make sure page request is POST. If not, deliver first page.
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            enroll = Enroll(email=form._raw_value('email'), course=Course(id=form._raw_value("course_id")))
            enroll.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse(form.errors)
    else:
        return HttpResponse('Illegal submit!!!')
