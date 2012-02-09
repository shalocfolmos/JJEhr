from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'JJEhr.views.home', name='home'),
    # url(r'^JJEhr/', include('JJEhr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^backoffice/index.html','backoffice.views.index'),
    url(r'^course/index.html','lesson.views.index',name='t'),
    url(r'^admin/', include(admin.site.urls))
#    url(r'^admin/', include(admin.site.urls))
)
