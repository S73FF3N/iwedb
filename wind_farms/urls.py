from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.WindFarmList.as_view(), name='windfarm_list'),
    url(r'^add/$', views.WindFarmCreate.as_view(), name='new_wind_farm'),
    #url(r'^add/contract/$', views.ContractCreate.as_view(), name='new_contract'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.windfarm_detail, name='windfarm_detail'),
]