#coding=utf-8
import types
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db import models
class CourseManager(models.Manager):
    # default show 10 courses per page
    __default_page_size = 10
    # Make sure page request is an int. If not, deliver first page.
    __default_current_no = 1
    def search(self, **kwargs):
        tempDict ={}
        for key in kwargs :
            value = kwargs.get(key)
            if type(value) == types.ListType:
                tempDict[key] = value[0]
            else:
                tempDict[key] = value
        course_set = {}
        try:
            pageNo = int(tempDict.get('page'))
        except (ValueError,KeyError,TypeError):
            pageNo = self.__default_current_no
        try:
            pageSize = int(tempDict.get('size'))
        except (ValueError,KeyError,TypeError):
            pageSize = self.__default_page_size
        try:
            course_set = super(CourseManager,self).get_query_set().filter()
            if tempDict.has_key('n'):
                course_set = course_set.filter(courseName__contains = tempDict.get('n'))
            if tempDict.has_key('s'):
                course_set = course_set.filter(courseSpeaker__contains = tempDict.get('s'))
            if tempDict.has_key('c'):
                course_set = course_set.filter(courseDescription__contains = tempDict.get('c'))
            #result_count = course_set.count()
            if tempDict.has_key('o') and tempDict.has_key('t'):
                if tempDict.get('t') == 'desc':
                    course_set = course_set.order_by('-%s' % (tempDict.get('o')))
                else:
                    course_set = course_set.order_by('%s' % (tempDict.get('o')))
            else:
                course_set =  course_set.order_by('-createDate')
            #course_set = course_set[(pageNo-1) * pageSize:pageSize]
            paginator = Paginator(course_set, pageSize)
            #paginator._count = result_count
            course_set = paginator.page(pageNo)
        except (EmptyPage, InvalidPage):
            # If page request (9999) is out of range, deliver last page of results.
            course_set = paginator.page(paginator.num_pages)
        except (KeyError):
            return course_set
        return course_set