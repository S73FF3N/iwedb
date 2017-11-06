from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^conventions/$', views.conventions, name='conventions'),
    url(r'^turbine_models', views.wec_typ_list, name='wec_typ_filter_list'),
    url(r'^add/$', views.WEC_TypCreate.as_view(), name='new_wec_typ'),
    url(r'^edit/(?P<pk>\d+)$', views.WEC_TypEdit.as_view(), name='wec_typ_edit'),
    url(r'^image/(?P<wec_typ_id>\d+)/$', views.ImageCreate.as_view(), name='new_image'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.wec_typ_detail, name='wec_typ_detail'),
]