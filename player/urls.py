from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', login_required(views.PlayerList.as_view()), name='player_list'),
    url(r'^add/$', login_required(views.PlayerCreate.as_view()), name='new_player'),
    url(r'^edit/(?P<pk>\d+)$', login_required(views.PlayerEdit.as_view()), name='player_edit'),
    url(r'^file/edit/(?P<pk>\d+)/(?P<player_id>\d+)/$', login_required(views.FileEdit.as_view()), name='edit_file'),
    url(r'^file/(?P<player_id>\d+)/$', login_required(views.FileCreate.as_view()), name='new_file'),
    url(r'^(?P<id>\d+)/(?P<slug>[-_\w]+)/add/employee/', login_required(views.PersonCreate.as_view()), name='new_person'),
    url(r'^edit/employee/(?P<pk>\d+)$', login_required(views.PersonEdit.as_view()), name='edit_person'),
    url(r'^sign-out/employee/(?P<id>\d+)$', login_required(views.sign_out_person), name='sign_out_person'),
    url(r'^comment/edit/(?P<pk>\d+)/(?P<model>[-_\w]+)/(?P<id>\d+)/$', login_required(views.CommentEdit.as_view()), name='edit_comment'),
    url(r'^comment/(?P<model>[-_\w]+)/(?P<id>\d+)/$', login_required(views.CommentCreate.as_view()), name='new_comment'),
    url(r'^(?P<id>\d+)/(?P<slug>[-_\w]+)/$', login_required(views.player_detail), name='player_detail'),
    url(r'^employee/(?P<id>\d+)$', login_required(views.person_detail), name='person_detail'),
    url(r'^ajax/validate_actor_name/$', views.validate_actor_name, name='validate_actor_name'),
]
