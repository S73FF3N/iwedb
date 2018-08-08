from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', login_required(views.ProjectList.as_view()), name='project_list'),
    url(r'^edit/(?P<pk>\d+)$', views.ProjectEdit.as_view(), name='project_edit'),
    url(r'^add/$', views.ProjectCreate.as_view(), name='new_project'),
    url(r'^comment/edit/(?P<pk>\d+)/(?P<project_id>\d+)/$', views.CommentEdit.as_view(), name='edit_comment'),
    url(r'^comment/(?P<project_id>\d+)/$', views.CommentCreate.as_view(), name='new_comment'),
    url(r'^export/$', views.ProjectList.export_xlsx, name='export'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', login_required(views.project_detail), name='project_detail'),
]