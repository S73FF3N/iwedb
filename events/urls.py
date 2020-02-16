from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', login_required(views.EventAndDateList.as_view()), name='event_list'),
    url(r'^comment/edit/(?P<pk>\d+)/(?P<event_id>\d+)/$', login_required(views.CommentEdit.as_view()), name='edit_comment'),
    url(r'^comment/(?P<event_id>\d+)/$', login_required(views.CommentCreate.as_view()), name='new_comment'),
    url(r'^date/add/(?P<event_id>\d+)$', login_required(views.DateCreate), name='date_add'),
    url(r'^create_dates/(?P<id>\d+)/$', login_required(views.create_dates), name='create_dates'),
    url(r'^edit/(?P<pk>\d+)$', login_required(views.EventEdit.as_view()), name='event_edit'),
    url(r'^add/$', login_required(views.EventCreate.as_view()), name='new_event'),
    url(r'^change-multiple-dates/(?P<pk>\d+)/$', login_required(views.ChangeMultipleDates), name='change_multiple_dates'),
    url(r'^(?P<id>\d+)/$', login_required(views.event_detail), name='event_detail'),
    #url(r'^date_list', login_required(views.DateList.as_view()), name='date_list'),
    url(r'^date/edit/(?P<pk>\d+)$', login_required(views.DateEdit.as_view()), name='date_update'),
    url(r'^date/delete/(?P<date>\d+)$', login_required(views.DateDelete), name='date_delete'),
    url(r'^export/$', views.EventAndDateList.export, name='export'),
]