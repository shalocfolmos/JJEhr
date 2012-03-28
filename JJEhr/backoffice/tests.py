# -*- coding: utf-8 -*-
from django.core import urlresolvers
from django.test.client import Client

from django.utils.unittest import TestCase

class ViewTest(TestCase):
    def should_add_course(self):
        c = Client()
        response = c.post(urlresolvers.reverse("backoffice:addCourse"))
        self.assertEqual(response.status_code, 200)


