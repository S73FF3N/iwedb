from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.component_type_list, name='component_type_list'),
    url(r'^gearbox-add/$', views.GearboxCreate.as_view(), name='new_gearbox'),
    url(r'^gearbox-edit/(?P<pk>\d+)$', views.GearboxEdit.as_view(), name='gearbox_edit'),
    url(r'^gearbox/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.gearbox_detail, name='gearbox_detail'),
    url(r'^generator-add/$', views.GeneratorCreate.as_view(), name='new_generator'),
    url(r'^generator-edit/(?P<pk>\d+)$', views.GeneratorEdit.as_view(), name='generator_edit'),
    url(r'^generator/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.generator_detail, name='generator_detail'),
    url(r'^tower-add/$', views.TowerCreate.as_view(), name='new_tower'),
    url(r'^tower-edit/(?P<pk>\d+)$', views.TowerEdit.as_view(), name='tower_edit'),
    url(r'^tower/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.gearbox_detail, name='tower_detail'),
    url(r'^image/(?P<component_id>\d+)/(?P<component_slug>[-\w]+)/$', views.ImageCreate.as_view(), name='component_image'),
]