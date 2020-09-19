from django.contrib import admin
from .models import Manufacturer, WEC_Typ, Image, Wind_Class
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class WEC_TypResources(resources.ModelResource):
    class Meta:
        model = WEC_Typ

class ManufacturerResources(resources.ModelResource):
    class Meta:
        model = Manufacturer

class Wind_ClassAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_editable = ['name']
admin.site.register(Wind_Class, Wind_ClassAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'source', 'content_type', 'object_id', 'content_object', 'available']
    list_editable = ['available', 'source']
admin.site.register(Image, ImageAdmin)

class ManufacturerAdmin(ImportExportModelAdmin):
    resource_class = ManufacturerResources

    list_display = ['name', 'id', 'slug', 'turbine_model_manufacturer']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Manufacturer, ManufacturerAdmin)


class WEC_TypAdmin(ImportExportModelAdmin):
    resource_class = WEC_TypResources

    list_display = ['name', 'slug', 'manufacturer', 'output_power', 'id', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'manufacturer']
    list_editable = ['output_power', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(WEC_Typ, WEC_TypAdmin)
