from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', login_required(views.WindFarmList.as_view()), name='windfarm_list'),
    url(r'^add/$', login_required(views.WindFarmCreate.as_view()), name='new_wind_farm'),
    url(r'^edit/(?P<pk>\d+)$', login_required(views.WindFarmEdit.as_view()), name='windfarm_edit'),
    url(r'^change-turbine-fields/(?P<pk>\d+)/(?P<slug>[-\w]+)/$', login_required(views.ChangeTurbineFields), name='change_turbine_fields'),
    url(r'^csv/$', views.WindFarmList.generate_csv, name='csv'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', login_required(views.windfarm_detail), name='windfarm_detail'),
    url(r'^ajax/validate_windfarm_name/$', views.validate_windfarm_name, name='validate_windfarm_name'),
]