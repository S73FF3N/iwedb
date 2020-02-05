from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
#from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'maintenance-mode/', include('maintenance_mode.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^turbine/', include('turbine.urls', namespace='turbines')),
    url(r'^wind_farms/', include('wind_farms.urls', namespace='wind_farms')),
    url(r'^player/', include('player.urls', namespace='player')),
    url(r'^projects/', include('projects.urls', namespace='projects')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^', include('polls.urls', namespace='polls')),
    url(r'^account/', include('account.urls')),
    )

#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns = [
#        url(r'^__debug__/', include(debug_toolbar.urls)),
#    ] + urlpatterns
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)