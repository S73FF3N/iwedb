from django.contrib import admin
from .models import Manufacturer, WEC_Typ
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class WEC_TypResources(resources.ModelResource):
    class Meta:
        model = WEC_Typ

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Manufacturer, ManufacturerAdmin)


class WEC_TypAdmin(ImportExportModelAdmin):
    resource_class = WEC_TypResources

    list_display = ['name', 'slug', 'manufacturer', 'output_power', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'manufacturer']
    list_editable = ['output_power', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(WEC_Typ, WEC_TypAdmin)
