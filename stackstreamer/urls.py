from django.conf.urls import patterns, include, url
import settings
from django.conf.urls.static import static

import stackorg.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'', include('stackorg.urls')),
    url(r'^$', 'stackstreamer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^datalist/','stackorg.views.datalist', name='datalist'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
