from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',

    url(r'^$', 'lesson.views.index'),
    url(r'^book/$', 'lesson.views.book_course'),
    url(r'^course/index.html', 'lesson.views.index'),
    url(r'^backoffice/login', 'django.contrib.auth.views.login', {'template_name': 'backoffice/login.html'}),

    url(r'^backoffice/course/(?P<courseId>\d+)$', 'backoffice.views.courseView'),
    url(r'^backoffice/course/delete/(?P<courseId>\d+)$', 'backoffice.views.delete_course'),
    url(r'^backoffice/logout', 'backoffice.views.admin_logout'),
    url(r'^backoffice/course/add', 'backoffice.views.addCourse'),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns(r'backoffice',
    url(r'^backoffice/export', r'views.export_notification_list'),
    url(r'^backoffice/index.html', r'views.displayCourseList'),
)

urlpatterns += patterns(r'event',
    url(r'^event/eventtype/add', r'views.event_type_add'),
    url(r'^event/eventtype/eventformcontent', r'views.ajax_content_html'),
    url(r'^event/eventtype/all', r'views.get_all_event_type'),
    url(r'^event/eventtype/delete/(?P<event_type_id>\d+)$', r'views.event_type_delete'),
)
