from django.contrib import admin

from .models import Turbine

class TurbineAdmin(admin.ModelAdmin):
    list_display = ['turbine_id', 'wind_farm', 'wec_manufacturer', 'wec_typ', 'available', 'created', 'updated']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('turbine_id',)}
admin.site.register(Turbine, TurbineAdmin)
