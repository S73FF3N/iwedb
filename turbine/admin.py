from django.contrib import admin
from .models import Turbine, Contract, ServiceLocation, Exclusion
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class TurbineResources(resources.ModelResource):
    class Meta:
        model = Turbine

class TurbineAdmin(ImportExportModelAdmin):
    resource_class = TurbineResources

    list_display = ['turbine_id', 'id', 'wind_farm', 'wec_typ', 'owner','hub_height', 'osm_id', 'offshore', 'available', 'created', 'updated']
    list_editable = ['offshore', 'hub_height', 'available', 'osm_id']
    list_filter = ['available', 'created', 'updated', 'wec_typ']
    prepopulated_fields = {'slug': ('turbine_id',)}
    search_fields = ('turbine_id', 'wind_farm__name',)
admin.site.register(Turbine, TurbineAdmin)

class ContractAdmin(admin.ModelAdmin):
    list_display = ['name', 'actor', 'start_date', 'end_date', 'active', 'created', 'updated']
    list_editable = ['active']
    search_fields = ('name',)
admin.site.register(Contract, ContractAdmin)

class ServiceLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'dwt', 'location_type', 'latitude', 'longitude', 'active', 'created', 'updated']
    list_editable = ['active']
    search_fields = ('name',)
admin.site.register(ServiceLocation, ServiceLocationAdmin)

class ExclusionAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Exclusion, ExclusionAdmin)
