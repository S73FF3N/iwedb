from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', login_required(views.TurbineList.as_view()), name='turbine_list'),
    url(r'^contract_list/$', login_required(views.ContractList.as_view()), name='contract_list'),
    url(r'^edit/(?P<pk>\d+)$', login_required(views.TurbineEdit.as_view()), name='turbine_edit'),
    url(r'^contract/edit/(?P<pk>\d+)$', login_required(views.ContractEdit.as_view()), name='contract_edit'),
    url(r'^duplicate_turbine/(?P<id>\d+)/(?P<slug>[-\w]+)/(?P<amount>\d+)/$', login_required(views.duplicate_turbine), name='duplicate_turbine'),
    url(r'^comment/edit/(?P<pk>\d+)/(?P<contract_id>\d+)/$', login_required(views.CommentEdit.as_view()), name='edit_comment'),
    url(r'^windfarm-autocomplete/$', views.WindFarmAutocomplete.as_view(), name='windfarm-autocomplete'),
    url(r'^wec-typ-autocomplete/$', views.WEC_TypAutocomplete.as_view(), name='wec-typ-autocomplete'),
    url(r'^manufacturer-autocomplete/$', views.ManufacturerAutocomplete.as_view(), name='manufacturer-autocomplete'),
    url(r'^actor-autocomplete/$', views.ActorAutocomplete.as_view(), name='actor-autocomplete'),
    url(r'^country-autocomplete/$', views.CountryAutocomplete.as_view(), name='country-autocomplete'),
    url(r'^turbineID-autocomplete/$', views.TurbineIDAutocomplete.as_view(), name='turbineID-autocomplete'),
    url(r'^person-autocomplete/$', views.PersonAutocomplete.as_view(), name='person-autocomplete'),
    url(r'^user-autocomplete/$', views.UserAutocomplete.as_view(), name='user-autocomplete'),
    url(r'^project-autocomplete/$', views.ProjectAutocomplete.as_view(), name='project-autocomplete'),
    url(r'^customer-relations-autocomplete/$', views.CustomerRelationAutocomplete.as_view(), name='customer-relations-autocomplete'),
    url(r'^offer-number-autocomplete/$', views.OfferNumberAutocomplete.as_view(), name='offer-number-autocomplete'),
    url(r'^terminated_contracts/$', login_required(views.TerminatedContracts.as_view()), name='terminated_contracts'),
    url(r'^add/$', login_required(views.TurbineCreate.as_view()), name='new_turbine'),
    url(r'^contract_csv/$', views.ContractList.generate_csv, name='contract_csv'),
    url(r'^add_contract/$', login_required(views.ContractCreate.as_view()), name='new_contract'),
    url(r'^contract/comment/(?P<contract_id>\d+)/$', login_required(views.CommentCreate.as_view()), name='new_comment'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', login_required(views.turbine_detail), name='turbine_detail'),
    url(r'^contract/(?P<id>\d+)/$', login_required(views.contract_detail), name='contract_detail'),
    url(r'^ajax/validate_turbine_id/$', views.validate_turbine_id, name='validate_turbine_id'),
    url(r'^ajax/validate_contract_name/$', views.validate_contract_name, name='validate_contract_name'),
    url(r'^ajax/terminate_contract/(?P<pk>\d+)/$', views.TerminateContract.as_view(), name='terminate_contract'),
]