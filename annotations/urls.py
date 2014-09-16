from django.conf.urls import patterns, include, url
import stackstreamer.settings
from django.conf.urls.static import static

from annotations.views import CreateFlagView, list_flags, delete_flag

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^flags/create/$', CreateFlagView.as_view(), name='flag_create'),
    url(r'^flags/list/$', list_flags, name='flag_list'),
    url(r'^flags/delete/(?P<id>.+)/', delete_flag, name='delete_flag'),

)
