from django.conf.urls import patterns, include, url
import stackorg.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stackstreamer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^datalist/','stackorg.views.datalist', name='datalist'),
    url(r'^admin/', include(admin.site.urls)),
)
