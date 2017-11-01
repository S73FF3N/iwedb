from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TurbineList.as_view(), name='turbine_list'),
    url(r'^edit/(?P<pk>\d+)$', views.TurbineEdit.as_view(), name='turbine_edit'),
    url(r'^windfarm-autocomplete/$', views.WindFarmAutocomplete.as_view(), name='windfarm-autocomplete'),
    url(r'^wec-typ-autocomplete/$', views.WEC_TypAutocomplete.as_view(), name='wec-typ-autocomplete'),
    url(r'^manufacturer-autocomplete/$', views.ManufacturerAutocomplete.as_view(), name='manufacturer-autocomplete'),
    url(r'^actor-autocomplete/$', views.ActorAutocomplete.as_view(), name='actor-autocomplete'),
    url(r'^turbine-autocomplete/$', views.TurbineAutocomplete.as_view(), name='turbine-autocomplete'),
    url(r'^country-autocomplete/$', views.CountryAutocomplete.as_view(), name='country-autocomplete'),
    url(r'^add/$', views.TurbineCreate.as_view(), name='new_turbine'),
    url(r'^add_contract/$', views.ContractCreate.as_view(), name='new_contract'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.turbine_detail, name='turbine_detail'),
]