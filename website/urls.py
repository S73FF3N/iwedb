from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^turbine/', include('turbine.urls', namespace='turbines')),
    url(r'^components/', include('components.urls', namespace='components')),
    url(r'^wind_farms/', include('wind_farms.urls', namespace='wind_farms')),
    url(r'^player/', include('player.urls', namespace='player')),
    url(r'^', include('polls.urls', namespace='polls')),
    url(r'^account/', include('account.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)