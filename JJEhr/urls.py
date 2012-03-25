from django.conf.urls.defaults import patterns, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'lesson.views.index'),
    url(r'^book/$', 'lesson.views.book_course'),
    url(r'^course/index.html', 'lesson.views.index'),
    url(r'^backoffice/login', 'django.contrib.auth.views.login', {'template_name': 'backoffice/login.html'}),
    url(r'^backoffice/index.html', 'backoffice.views.displayCourseList'),
    url(r'^backoffice/course/(?P<courseId>\d+)$', 'backoffice.views.courseView'),
    url(r'^backoffice/course/delete/(?P<courseId>\d+)$', 'backoffice.views.delete_course'),
    url(r'^backoffice/logout', 'backoffice.views.admin_logout'),
    url(r'^backoffice/course/add', 'backoffice.views.addCourse'),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns(r'backoffice',
    url(r'^backoffice/export', r'views.export_notification_list')
)
