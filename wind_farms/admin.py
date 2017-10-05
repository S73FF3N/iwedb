from django.contrib import admin
from .models import WindFarm, Country#, Contract
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class WindFarmResources(resources.ModelResource):
    class Meta:
        model = WindFarm

class CountryResources(resources.ModelResource):
    class Meta:
        model = Country

class CountryAdmin(ImportExportModelAdmin):
    ressource_class = CountryResources

    list_display = ['name']
admin.site.register(Country, CountryAdmin)


class WindFarmAdmin(ImportExportModelAdmin):
    resource_class = WindFarmResources

    list_display = ['name', 'slug', 'country', 'city', 'available', 'created', 'updated'] #, 'manufacturer', 'wec_typ', 'amount_turbines'
    list_filter = ['available', 'created', 'updated', 'country'] #, 'wec_typ'
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(WindFarm, WindFarmAdmin)

#class ContractAdmin(admin.ModelAdmin):
#    list_display = ['windfarm', 'actor', 'contract_type', 'start_date', 'end_date']
#admin.site.register(Contract, ContractAdmin)