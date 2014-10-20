from django.conf.urls import patterns, include, url
import settings
from django.conf.urls.static import static

from tastypie.api import Api
from api.resources import StackResource, FlagResource, ArrowResource

import stackorg.views

from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(StackResource())
v1_api.register(FlagResource())
v1_api.register(ArrowResource())

urlpatterns = patterns('',
    # Examples:
    url(r'', include('stackorg.urls')),
    url(r'', include('exportroi.urls')),
    url(r'', include('annotations.urls')),
    url(r'^$', 'stackstreamer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^datapath/(?P<uuid>.+)/', 'stackstreamer.views.get_stack_data_path', name='get_stack_data_path'),
    url(r'^verifyaccess/(?P<access_token>.+)/(?P<response_token>.+)/', 'stackstreamer.views.verify_access_token', name='verify_access_token'),
    url(r'^datalist/','stackorg.views.datalist', name='datalist'),
    url(r'^accounts/login/$', 'stackstreamer.views.login_user', name='login'),
    url(r'^accounts/logout/$', 'stackstreamer.views.logout_user', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
