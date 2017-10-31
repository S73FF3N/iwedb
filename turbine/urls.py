from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.TurbineList.as_view(), name='turbine_list'),
    url(r'^add/$', views.TurbineCreate.as_view(), name='new_turbine'),
    url(r'^add_contract/$', views.ContractCreate.as_view(), name='new_contract'),
    url(r'^edit/(?P<pk>\d+)$', views.TurbineEdit.as_view(), name='turbine_edit'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.turbine_detail, name='turbine_detail'),
]