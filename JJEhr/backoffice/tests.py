# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core import urlresolvers

from django.test import TestCase
from JJEhr.lesson.models import Course

class ViewTest(TestCase):
    USER_NAME = "sam"
    USER_PASSWORD = "123456"
    ADD_COURSE_URL = urlresolvers.reverse("backoffice.views.addCourse")
    INDEX_URL = urlresolvers.reverse("backoffice.views.displayCourseList")

    def setUp(self):
        User.objects.create_user(ViewTest.USER_NAME, password=ViewTest.USER_PASSWORD, email="test@test.com")
        self.client.login(username=ViewTest.USER_NAME, password=ViewTest.USER_PASSWORD)

    def test_should_add_course_to_db(self):
        response = self.client.post(ViewTest.ADD_COURSE_URL, {"courseName": "courseName", "courseTime": "12",
                                                              "courseDescription": "courseDescription",
                                                              "courseArrange": "courseArrange",
                                                              "courseSpeaker": "courseSpeaker",
                                                              "enrollStartTime": "2012-02-11",
                                                              "courseStartTime": "2012-02-15",
                                                              "enrollEndTime": "2012-02-17",
                                                              "maxTraineeAmount": 11})
        course = Course.objects.filter(courseName__exact="courseName")[0]
        self.assertEqual("courseName", course.courseName)
        self.assertRedirects(response, expected_url=ViewTest.INDEX_URL)
