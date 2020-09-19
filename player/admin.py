from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

from .models import Player, Sector, Person, File, MailingList

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from datetime import datetime
import xlwt

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

class MailingListResources(resources.ModelResource):
    class Meta:
        model = MailingList

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

    list_display = ['name', 'first_name', 'id', 'function', 'mail', 'phone', 'available', 'created', 'updated']
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

class MailingListAdmin(ImportExportModelAdmin):
    actions = ['mailing_list_export',]
    resource_class = MailingListResources

    list_display = ['id', 'name',]
    search_fields = ('name',)

    def mailing_list_export(self, request, queryset):
        filename = "mailing-list-export-{}.xls".format(datetime.now().replace(microsecond=0).isoformat())
        response = HttpResponse(content_type='applications/vnd.ms-excel')
        response['Content-Disposition'] = 'attachement; filename="{}"'.format(filename)
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Mailing List")
        row_num = 0
        columns = [(_('Company'),5000), (_('Title'), 5000), (_('First Name'), 5000), (_('Last Name'), 3000), (_('Address'), 5000), (_('Postal Code'), 3000), (_('City'), 3000), (_('Country'), 3000), (_('Mail'), 7000), (_('Postal Communication'), 5000), (_('Mailing List'), 5000)]
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, str(columns[col_num][0]), font_style)
            ws.col(col_num).width = columns[col_num][1]
        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        date_style = xlwt.XFStyle()
        date_style.num_format_str = 'D-MMM-YY'
        font_styles = [font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style]
        qs = Person.objects.filter(mailing_list__in=queryset)
        for obj in qs:
            row_num += 1
            if obj.gender == "male":
                gender = "Herr"
            elif obj.gender == "female":
                gender = "Frau"
            else:
                gender = " "
            row = [obj.company_name, gender, obj.first_name, obj.name, obj.adress, obj.postal_code, obj.city, obj.country.name, obj.mail, obj.postal_communication, obj.mailing_list_name]
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_styles[col_num])
        wb.save(response)
        return response

admin.site.register(MailingList, MailingListAdmin)
