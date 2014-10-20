from django.conf.urls import patterns, include, url
import stackstreamer.settings
from django.conf.urls.static import static

import stackorg.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^list/', 'stackorg.views.list_all_stacks', name='list_all_stacks'),
    url(r'^projects/', 'stackorg.views.list_all_projects', name='list_all_projects'),
    url(r'^listexports/(?P<stackid>.+)/$', 'stackorg.views.list_exports', name='list_exports'),
    url(r'^liststacks/(?P<projectid>.+)/$', 'stackorg.views.list_project_stacks', name='list_project_stacks'),
    # url(r'^blog/', include('blog.urls')),
)
