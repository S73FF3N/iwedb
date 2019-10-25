from django.contrib import admin
from .models import Event, Date

class EventAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ('title',)
admin.site.register(Event, EventAdmin)

class DateAdmin(admin.ModelAdmin):
    list_display = ['date']
    search_fields = ('date',)
admin.site.register(Date, DateAdmin)