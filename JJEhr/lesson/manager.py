#coding=utf-8
from django.core.paginator import Paginator, EmptyPage, InvalidPage, Page
from django.db import models
import types

class CourseManager(models.Manager):
    # default show 10 courses per page
    __default_page_size = 10
    # Make sure page request is an int. If not, deliver first page.
    __default_current_no = 1

    __default_page_range = 10

    def search(self, **kwargs):
        tempDict = {}
        for key in kwargs:
            value = kwargs.get(key)
            if type(value) == types.ListType:
                tempDict[key] = value[0]
            else:
                tempDict[key] = value
        pageNo, pageSize, pageRange = self.__validateCondition(**tempDict)
        try:
            course_set = super(CourseManager, self).get_query_set().filter()
            course_set = self.__buildSearchCondition(course_set, **tempDict)
            paginatorEx = PaginatorEx(course_set, QueryCondition(pageSize, pageRange, pageNo, **tempDict))
            course_set = paginatorEx.page()
        except (EmptyPage, InvalidPage):
            # If page request (9999) is out of range, deliver last page of results.
            course_set = paginatorEx.page()
        except (KeyError):
            return course_set
        return course_set

    def __buildSearchCondition(self, course_set, **kwargs):
        try:
            for key, value in kwargs.items():
                course_set = self.__switch(course_set, key, value)
            if kwargs.has_key('searchType') and kwargs.has_key('searchContent'):
                course_set = self.__switch(course_set, kwargs.get('searchType'), kwargs.get('searchContent'))
            if kwargs.has_key('o') and kwargs.has_key('t'):
                if kwargs.get('t') == 'desc':
                    course_set = course_set.order_by('-%s' % (kwargs.get('o')))
                else:
                    course_set = course_set.order_by('%s' % (kwargs.get('o')))
            else:
                course_set = course_set.order_by('-createDate')
        except Exception:
            pass
        return course_set

    def __switch(self, course_set, key, value):
        try:
            if key == 'n':
                course_set = course_set.filter(courseName__contains=value)
            if key == 's':
                course_set = course_set.filter(courseSpeaker__contains=value)
            if key == 'c':
                course_set = course_set.filter(courseDescription__contains=value)
            if key == 'b':
                course_set = course_set.filter(event_type__type_name__contains=value)
        except Exception:
            pass
        return course_set

    def __validateCondition(self, **kwargs):
        try:
            pageNo = int(kwargs.get('page'))
        except (ValueError, KeyError, TypeError):
            pageNo = self.__default_current_no
        try:
            pageSize = int(kwargs.get('size'))
        except (ValueError, KeyError, TypeError):
            pageSize = self.__default_page_size
        try:
            pageRange = int(kwargs.get('range'))
        except (ValueError, KeyError, TypeError):
            pageRange = self.__default_page_range
        return pageNo, pageSize, pageRange


class QueryCondition(object):
    def __init__(self, page_size, page_range_size, current_page_no, **kwargs):
        self.page_size = page_size
        self.page_range_size = page_range_size
        self.current_page_no = current_page_no
        self.kwargs = kwargs

    def parseQueryString(self):
        query_string = ''
        for key in self.kwargs:
            if key == 'page':
                continue
            query_string += "&%s=%s" % (key, self.kwargs.get(key))
        return query_string

    queryStr = property(parseQueryString)


class PaginatorEx(Paginator):
    def __init__(self, object_list, query_condition):
        super(PaginatorEx, self).__init__(object_list, query_condition.page_size)
        self.query_condition = query_condition

    def page(self):
        "Returns a Page object for the given 1-based page number."
        number = self.query_condition.current_page_no
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return PageEx(self.object_list[bottom:top], self, self.query_condition)


class PageEx(Page):
    def __repr__(self):
        return '<Page %s of %s>' % (self.query_condition.current_page_no, self.paginator.num_pages)

    def __init__(self, object_list, paginator, query_condition):
        super(PageEx, self).__init__(object_list, query_condition.current_page_no, paginator)
        self.pageCount = paginator.num_pages
        self.query_condition = query_condition

    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        page_range_size = self.query_condition.page_range_size

        if self.pageCount < page_range_size:
            startPageIndex = 1
            endPageIndex = self.pageCount
        elif self.number <= (page_range_size / 2) + 1:
            startPageIndex = 1
            endPageIndex = page_range_size
        else:
            startPageIndex = self.number - (page_range_size / 2)
            endPageIndex = self.number + (page_range_size / 2)
        if endPageIndex > self.pageCount:
            endPageIndex = self.pageCount
            startPageIndex = self.pageCount - page_range_size + 1
        if startPageIndex <= 0:
            startPageIndex = 1

        return range(startPageIndex, endPageIndex + 1)

    page_range = property(_get_page_range)

    def home_page(self):
        if self.pageCount > 1 and self.number != 1:
            return True
        return False

    def end_page(self):
        if self.pageCount > 1 and self.number < self.pageCount - 1:
            return True
        return False

    def queryStr(self):
        return self.query_condition.queryStr

    def pageSize(self):
        return self.query_condition.page_size

    def pageRangeSize(self):
        return self.query_condition.page_range_size

    def currentPageNo(self):
        return self.query_condition.current_page_no


class tempMapping(object):
    __default_mapping_dict = {'n': u'课程名', 's': u'主讲人', 'c': u'内 容', 'b': u'类 型'}

    def getAllSearchType(self):
        return self.__default_mapping_dict

    def getSearchType(self, key):
        return self.__default_mapping_dict.get(key, '')