from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', login_required(views.PlayerList.as_view()), name='player_list'),
    url(r'^add/$', views.PlayerCreate.as_view(), name='new_player'),
    url(r'^edit/(?P<pk>\d+)$', views.PlayerEdit.as_view(), name='player_edit'),
    url(r'^(?P<id>\d+)/(?P<slug>[-_\w]+)/add/employee/', views.PersonCreate.as_view(), name='new_person'),
    url(r'^edit/employee/(?P<pk>\d+)$', views.PersonEdit.as_view(), name='edit_person'),
    url(r'^comment/edit/(?P<pk>\d+)/(?P<person_id>\d+)/$', views.CommentEdit.as_view(), name='edit_comment'),
    url(r'^comment/(?P<person_id>\d+)/$', views.CommentCreate.as_view(), name='new_comment'),
    url(r'^(?P<id>\d+)/(?P<slug>[-_\w]+)/$', login_required(views.player_detail), name='player_detail'),
    url(r'^employee/(?P<id>\d+)$', login_required(views.person_detail), name='person_detail'),
]
