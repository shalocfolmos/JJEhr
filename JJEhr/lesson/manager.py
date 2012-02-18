#coding=utf-8
import types
from django.core.paginator import Paginator, EmptyPage, InvalidPage, Page
from django.db import models
class CourseManager(models.Manager):
    # default show 10 courses per page
    __default_page_size = 2
    # Make sure page request is an int. If not, deliver first page.
    __default_current_no = 1

    __default_page_range = 3

    def search(self, **kwargs):
        tempDict ={}
        for key in kwargs :
            value = kwargs.get(key)
            if type(value) == types.ListType:
                tempDict[key] = value[0]
            else:
                tempDict[key] = value
        result = {}
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
            paginatorEx = PaginatorEx(course_set, pageSize)
            course_set = paginatorEx.page(pageNo,self.__default_page_range)
        except (EmptyPage, InvalidPage):
            # If page request (9999) is out of range, deliver last page of results.
            course_set = paginatorEx.page(paginatorEx.num_pages,self.__default_page_range)
        except (KeyError):
            return course_set

        return course_set


class PaginatorEx(Paginator):

    def page(self, number,page_range):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return PageEx(self.object_list[bottom:top], number, self, page_range)

class PageEx(Page):

    def __init__(self, object_list, number, paginator, page_range_size):
        super(PageEx, self).__init__(object_list, number, paginator)
        self.pageCount = paginator.num_pages
        self.page_range_size = page_range_size


    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        if self.pageCount < self.page_range_size:
            startPageIndex = 1
            endPageIndex = self.pageCount
        elif self.number <= (self.page_range_size/2)+1:
            startPageIndex = 1
            endPageIndex = self.page_range_size
        else:
            startPageIndex = self.number - (self.page_range_size/2)
            endPageIndex = self.number + (self.page_range_size/2)
        if endPageIndex > self.pageCount:
            endPageIndex = self.pageCount
            startPageIndex = self.pageCount- self.page_range_size +1
        if startPageIndex <=0:
             startPageIndex = 1

        return range(startPageIndex, endPageIndex + 1)
    page_range = property(_get_page_range)

    def home_page(self):
        if self.pageCount > 1 and self.number != 1:
            return True
        return False

    def end_page(self):
        if self.pageCount > 1 and self.number < self.pageCount-1:
            return True
        return False


