from django.contrib import admin
from .models import Player, Sector, Person, File

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

class PlayerResources(resources.ModelResource):
    name = Field(attribute='name', column_name='Actor')
    adress = Field(attribute='adress', column_name='Address')
    postal_code = Field(attribute='postal_code', column_name='Postal Code')
    city = Field(attribute='city', column_name='City')
    country__name = Field(attribute='country__name', column_name='Country')
    phone = Field(attribute='phone', column_name='Phone')
    mail = Field(attribute='Mail', column_name='Mail')
    web = Field(attribute='web', column_name='Web')
    sector__name = Field(attribute='sector__name', column_name='Sector')
    head_organisation__name = Field(attribute='head_organisation__name', column_name='Head Organisation')
    class Meta:
        model = Player
        fields = ('name', 'adress', 'postal_code', 'city', 'country__name', 'phone', 'mail', 'web', 'sector__name', 'head_organisation__name')

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


class FileResources(resources.ModelResource):
    class Meta:
        model = File

class FileAdmin(ImportExportModelAdmin):
    resource_class = FileResources

    list_display = ['id', 'name', 'content_type', 'object_id', 'available', 'created', 'created_by']
    list_editable = ['available']
    list_filter = ['available']
    search_fields = ('name',)
admin.site.register(File, FileAdmin)
