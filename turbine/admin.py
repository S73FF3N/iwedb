from django.contrib import admin
from .models import Turbine, Contract
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class TurbineResources(resources.ModelResource):
    class Meta:
        model = Turbine

class TurbineAdmin(ImportExportModelAdmin):
    resource_class = TurbineResources

    list_display = ['turbine_id', 'wind_farm', 'wec_manufacturer', 'wec_typ', 'available', 'created', 'updated']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('turbine_id',)}
admin.site.register(Turbine, TurbineAdmin)

class ContractAdmin(admin.ModelAdmin):
    list_display = ['turbine', 'actor', 'contract_type', 'start_date', 'end_date', 'available', 'created', 'updated']
    list_editable = ['available']
admin.site.register(Contract, ContractAdmin)
