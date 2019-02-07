from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', login_required(views.ProjectList.as_view()), name='project_list'), #/(?P<per_page>\d+)/
    url(r'^edit/(?P<pk>\d+)$', login_required(views.ProjectEdit.as_view()), name='project_edit'),
    url(r'^add/$', login_required(views.ProjectCreate.as_view()), name='new_project'),
    url(r'^comment/edit/(?P<pk>\d+)/(?P<project_id>\d+)/$', login_required(views.CommentEdit.as_view()), name='edit_comment'),
    url(r'^project_to_contract/(?P<id>\d+)/(?P<slug>[-\w]+)/$', login_required(views.project_to_contract), name='project_to_contract'),
    url(r'^comment/(?P<project_id>\d+)/$', login_required(views.CommentCreate.as_view()), name='new_comment'),
    url(r'^export/$', views.ProjectList.export_xlsx, name='export'),
    url(r'^csv/$', views.ProjectList.generate_csv, name='csv'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', login_required(views.project_detail), name='project_detail'),
    url(r'^total_volume_report/$', login_required(views.TotalVolumeReport.as_view()), name='total_volume_report'),
    url(r'^calculation_tool/$', login_required(views.Calculation_ToolList.as_view()), name='calculation_tool'),
    url(r'^scada_information/(?P<id>\d+)/(?P<slug>[-\w]+)/$', login_required(views.create_pdf_scada_information), name='scada_information'),
    url(r'^ajax/validate_project_name/$', views.validate_project_name, name='validate_project_name'),
    #url(r'^ajax/surrounding_contracts/$', views.surrounding_contracts, name="surrounding_contracts"),
]