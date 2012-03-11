from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'JJEhr.views.home', name='home'),
    # url(r'^JJEhr/', include('JJEhr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^backoffice/index.html','backoffice.views.index'),
    url(r'^$', 'lesson.views.index'),
    url(r'^book/$', 'lesson.views.book_course'),
    url(r'^course/index.html', 'lesson.views.index'),
    url(r'^backoffice/login', 'django.contrib.auth.views.login', {'template_name': 'backoffice/login.html'}),
    url(r'^backoffice/index.html', 'backoffice.views.displayCourseList'),
    url(r'^backoffice/course/(?P<courseId>\d+)$', 'backoffice.views.courseView'),
    url(r'^backoffice/course/delete/(?P<courseId>\d+)$', 'backoffice.views.delete_course'),
    url(r'^backoffice/logout', 'backoffice.views.admin_logout'),
    url(r'^backoffice/course/add', 'backoffice.views.addCourse'),
    url(r'^backoffice/email', "backoffice.views.send_notification_email"),
    url(r'^admin/', include(admin.site.urls))
)

urlpatterns += staticfiles_urlpatterns()
