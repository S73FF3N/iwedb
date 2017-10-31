from django.contrib import admin
from .models import WindFarm, Country
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

    list_display = ['name', 'id']
admin.site.register(Country, CountryAdmin)


class WindFarmAdmin(ImportExportModelAdmin):
    resource_class = WindFarmResources

    list_display = ['name', 'slug', 'country', 'city', 'available', 'created', 'updated', 'offshore']
    list_filter = ['available', 'created', 'updated', 'country', 'offshore']
    list_editable = ['available', 'offshore']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(WindFarm, WindFarmAdmin)
