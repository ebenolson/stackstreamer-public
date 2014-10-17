from django.contrib.auth.decorators import login_required

from django.conf.urls import patterns, include, url
import stackstreamer.settings
from django.conf.urls.static import static

import stackorg.views

from exportroi.views import CreateDataExport

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^export/fullslice/(?P<uuid>.+)/(?P<slice>.+)/', 'exportroi.views.export_full_slice', name='export_full_slice'),
    url(r'^export/snapshot/(?P<uuid>.+)/(?P<slice>.+)/(?P<zoom>.+)/(?P<x0>.+)/(?P<y0>.+)/(?P<x1>.+)/(?P<y1>.+)', 
        'exportroi.views.export_snapshot', name='export_snapshot'),
    url(r'^export/dataexport/$', login_required()(CreateDataExport.as_view()), name='create_data_export'),
    # url(r'^blog/', include('blog.urls')),
)
