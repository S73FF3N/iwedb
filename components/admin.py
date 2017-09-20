from django.contrib import admin
from .models import ComponentType, Component

class ComponentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(ComponentType, ComponentTypeAdmin)


class ComponentAdmin(admin.ModelAdmin):
    list_display = ['component_type', 'name', 'slug', 'manufacturer', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'manufacturer']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Component, ComponentAdmin)