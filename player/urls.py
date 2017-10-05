from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.PlayerList.as_view(), name='player_list'),
    url(r'^add/$', views.PlayerCreate.as_view(), name='new_player'),
    url(r'^(?P<player_slug>[-\w]+)/$', views.PlayerList.as_view(), name='player_table'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.player_detail, name='player_detail'),
]
