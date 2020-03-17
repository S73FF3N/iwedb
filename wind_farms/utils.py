from django.db.models import Min, Case, When
from django.core import serializers
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from django_tables2 import SingleTableView
import serpy
from datetime import datetime
import xlwt

from .models import WindFarm

class WindFarmSerializer(serpy.Serializer):
    pk = serpy.IntField()
    slug = serpy.Field()
    latitude = serpy.Field()
    longitude = serpy.Field()
    name = serpy.Field()

class PagedFilteredTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset().filter(available=True).select_related('country').prefetch_related('turbine_set').annotate(first_com_date=Case(When(turbine__commisioning_year__isnull=False, then=Min('turbine__commisioning_year'))))
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.request.session['windfarm_json'] = serializers.serialize('json', self.filter.qs, fields=('pk'))
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(PagedFilteredTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    return context

    @classmethod
    def generate_csv(cls, request):
        filename = "{}-windfarms-export.xls".format(datetime.now().replace(microsecond=0).isoformat())
        response = HttpResponse(content_type='applications/vnd.ms-excel')
        response['Content-Disposition'] = 'attachement; filename="{}"'.format(filename)
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Project Overview")
        row_num = 0
        columns = [(u'Name',5000), (u'alt. Name', 5000), ('Country', 5000), ('Postal Code', 3000), ('City', 5000), ('Latitude', 3000), ('Longitude', 3000), ('Offshore', 3000), ('Description', 7000), ('Amount WTG', 5000), ('Turbine Models', 5000)]
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            ws.col(col_num).width = columns[col_num][1]
        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        date_style = xlwt.XFStyle()
        date_style.num_format_str = 'D-MMM-YY'
        font_styles = [font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style]
        deserialized = list(serializers.deserialize('json', request.session.get('windfarm_json')))
        pk_list = []
        for p in deserialized:
            pk_list.append(p.object.pk)
        queryset = WindFarm.objects.filter(pk__in=pk_list)
        for obj in queryset:
            row_num += 1
            row = [obj.name, obj.second_name, obj.country.name, obj.postal_code, obj.city, obj.latitude, obj.longitude, obj.offshore, obj.description, obj.amount_turbines_in_production, obj.wind_farm_wec_types_name]
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_styles[col_num])
        wb.save(response)
        return response