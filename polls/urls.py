from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^map/$', views.map, name='map'),
    url(r'^turbine_models', login_required(views.WEC_TypList.as_view()), name='wec_typ_filter_list'),
    url(r'^csv/$', views.WEC_TypList.generate_csv, name='csv'),
    url(r'^conventions/$', views.conventions, name='conventions'),
    url(r'^add/$', login_required(views.WEC_TypCreate.as_view()), name='new_wec_typ'),
    url(r'^edit/(?P<pk>\d+)$', login_required(views.WEC_TypEdit.as_view()), name='wec_typ_edit'),
    url(r'^image/(?P<wec_typ_id>\d+)/$', login_required(views.ImageCreate.as_view()), name='new_image'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', login_required(views.wec_typ_detail), name='wec_typ_detail'),
]