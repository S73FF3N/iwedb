from django.conf.urls import url
#from django_filters.views import FilterView
#from .filters import WEC_TypFilter
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^turbine_models', views.wec_typ_list, name='wec_typ_filter_list'),
    #url(r'^turbine_models', FilterView.as_view(filterset_class=WEC_TypFilter, template_name='polls/wec_typ/list.html'), name='wec_typ_filter_list'),
    url(r'^add/$', views.WEC_TypCreate.as_view(), name='new_wec_typ'),
    url(r'^edit/(?P<pk>\d+)$', views.WEC_TypEdit.as_view(), name='wec_typ_edit'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.wec_typ_detail, name='wec_typ_detail')
]