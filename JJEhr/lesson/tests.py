"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import datetime

from django.test import TestCase
from JJEhr.lesson.models import Course

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
    #
    def test_save_course(self):
        p = Course(courseName='test',courseTime=2,startTime=datetime.now(),maxTraineeAmount=2,courseSpeaker='evan')
        p.save()
