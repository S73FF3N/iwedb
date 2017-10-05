from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.turbine_detail, name='turbine_detail'),
]