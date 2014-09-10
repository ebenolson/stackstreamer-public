from django.conf.urls import patterns, include, url
import settings
from django.conf.urls.static import static

import stackorg.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'', include('stackorg.urls')),
    url(r'', include('exportroi.urls')),
    url(r'^$', 'stackstreamer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^datapath/(?P<uuid>.+)/', 'stackstreamer.views.get_stack_data_path', name='get_stack_data_path'),
    url(r'^verifyaccess/(?P<access_token>.+)/(?P<response_token>.+)/', 'stackstreamer.views.verify_access_token', name='verify_access_token'),
    url(r'^datalist/','stackorg.views.datalist', name='datalist'),
    url(r'^login/$', 'stackstreamer.views.login_user', name='login'),
    url(r'^logout/$', 'stackstreamer.views.logout_user', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
