from django.conf.urls import patterns, include, url
import stackstreamer.settings
from django.conf.urls.static import static

from annotations.views import CreateFlagView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^flags/create/$', CreateFlagView.as_view(),
        name='flag_list'),
)
