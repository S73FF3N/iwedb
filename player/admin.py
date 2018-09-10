from django.contrib import admin
from .models import Player, Sector, Person
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class PlayerResources(resources.ModelResource):
    class Meta:
        model = Player

class SectorResources(resources.ModelResource):
    class Meta:
        model = Sector

class PersonResources(resources.ModelResource):
    class Meta:
        model = Person

class PlayerAdmin(ImportExportModelAdmin):
    resource_class = PlayerResources

    list_display = ['name', 'slug', 'id', 'country', 'city', 'adress', 'postal_code', 'mail', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'postal_code', 'country']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
admin.site.register(Player, PlayerAdmin)

class PersonAdmin(ImportExportModelAdmin):
    resource_class = PersonResources

    list_display = ['name', 'id', 'function', 'mail', 'phone', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available']
    search_fields = ('name',)
admin.site.register(Person, PersonAdmin)

class SectorAdmin(ImportExportModelAdmin):
    resource_class = SectorResources

    list_display = [ 'id', 'name']
admin.site.register(Sector, SectorAdmin)
