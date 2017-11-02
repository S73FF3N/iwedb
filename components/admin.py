from django.contrib import admin
from .models import Gearbox, Generator, Tower

class GearboxAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'manufacturer', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'manufacturer']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Gearbox, GearboxAdmin)

class GeneratorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'manufacturer', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'manufacturer']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Generator, GeneratorAdmin)

class TowerAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'manufacturer', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'manufacturer']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Tower, TowerAdmin)