from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.component_type_list, name='component_type_list'),
    url(r'^(?P<component_type_slug>[-\w]+)/$', views.component_type_list, name='component_list_by_component_type'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.component_detail, name='component_detail'),
]