from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.component_type_list, name='component_type_list'),
    url(r'^add/$', views.ComponentCreate.as_view(), name='new_component'),
    url(r'^edit/(?P<pk>\d+)$', views.ComponentEdit.as_view(), name='component_edit'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.component_detail, name='component_detail'),
]