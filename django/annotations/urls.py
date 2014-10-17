from django.conf.urls import patterns, include, url
import stackstreamer.settings
from django.conf.urls.static import static

from annotations.views import CreateFlagView, list_flags, delete_flag, edit_flag_text, CreateArrowView, list_arrows, delete_arrow, edit_arrow_text, marker_list

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^flags/create/$', CreateFlagView.as_view(), name='flag_create'),
    url(r'^flags/list/(?P<stack>.+)/$', list_flags, name='flag_list'),
    url(r'^flags/delete/(?P<id>.+)/', delete_flag, name='delete_flag'),
    url(r'^flags/edit/', edit_flag_text, name='edit_flag_text'),

    url(r'^arrows/create/$', CreateArrowView.as_view(), name='arrow_create'),
    url(r'^arrows/list/(?P<stack>.+)/$', list_arrows, name='arrow_list'),
    url(r'^arrows/markers/(?P<stack>.+)/$', marker_list, name='marker_list'),
    url(r'^arrows/delete/(?P<id>.+)/', delete_arrow, name='delete_arrow'),
    url(r'^arrows/edit/', edit_arrow_text, name='edit_arrow_text'),

)
