from django.contrib.auth.models import User
from JJEhr.survey.models import StaffProfile

__author__ = 'sam-sun'


user=User.objects.create_user(username="sam.sun1",password="123456",email="sam.sun@jinjiang.com")
user.is_staff=True
user.is_active=True
user.save()
staff = StaffProfile(user=user,division="IT")
staff.save()



