from django.contrib.auth.models import User
from JJEhr.survey.models import StaffProfile, SurveyLog

user=User.objects.create_user(username="sam.sun1",password="123456",email="sam.sun@jinjiang.com")
user.is_staff=True
user.is_active=True
user.save()
staff = StaffProfile(user=user,division="IT")
staff.save()
user=User.objects.create_user(username="sam.sun2",password="123456",email="sam.sun@jinjiang.com")
user.is_staff=True
user.is_active=True
user.save()
staff = StaffProfile(user=user,division="CC")
staff.save()
user=User.objects.create_user(username="sam.sun3",password="123456",email="sam.sun@jinjiang.com")
user.is_staff=True
user.is_active=True
user.save()
staff = StaffProfile(user=user,division="SALE")
staff.save()


SurveyLog.objects.get(id=1)

#6d964c4e34ed81dc926254f195781e5d


