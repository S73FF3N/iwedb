from django.contrib import admin
from .models import Player, Sector
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class PlayerResources(resources.ModelResource):
    class Meta:
        model = Player

class PlayerAdmin(ImportExportModelAdmin):
    resource_class = PlayerResources

    list_display = ['name', 'slug', 'country', 'city', 'adress', 'postal_code', 'mail', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'postal_code', 'country']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Player, PlayerAdmin)

class SectorAdmin(admin.ModelAdmin):
    list_display = [ 'name']
admin.site.register(Sector, SectorAdmin)
