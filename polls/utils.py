from django.core import serializers
from django.http import HttpResponse
from django.db.models import Count
from django.views.generic.list import ListView

from datetime import datetime
import xlwt

from .models import WEC_Typ, Image

class FilteredView(ListView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(FilteredView, self).get_queryset().filter(available=True).annotate(amount_turbines=Count('turbine'))
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.request.session['search_queryset'] = serializers.serialize('json', self.filter.qs, fields=('pk'))
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(FilteredView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    urls = {wec_type.id : wec_type.get_absolute_url() for wec_type in self.filter.qs}
	    images = {}
	    images_qs = {}
	    img_objects = Image.objects.filter(content_type=9, available=True)
	    for img in img_objects:
	        if img.object_id not in images_qs:
	            images_qs[img.object_id] = img.file.url
	        else:
	            pass
	    wec_types_id = self.filter.qs.values_list('id', flat=True)
	    for wec_type in wec_types_id:
	        try:
	            images[wec_type] = images_qs[wec_type]
	        except:
	            images[wec_type] = '/static/img/no_image.png'
	    amount = {w.id:w.amount_turbines for w in self.filter.qs}
	    filter_count = self.filter.qs.count()
	    context['urls'] = urls
	    context['images'] = images
	    context["filter_count"] = filter_count
	    context["amount"] = amount
	    return context

    @classmethod
    def generate_csv(cls, request):
        filename = "{}-turbine-model-export.xls".format(datetime.now().replace(microsecond=0).isoformat())
        response = HttpResponse(content_type='applications/vnd.ms-excel')
        response['Content-Disposition'] = 'attachement; filename="{}"'.format(filename)
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Turbine Model Overview")
        row_num = 0
        columns = [(u'Manufacturer',5000), (u'Model', 5000), (u'Power Output', 5000), (u'Amount of contracted turbines', 5000), (u'Serviced by DWT', 3000)]
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            ws.col(col_num).width = columns[col_num][1]
        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        deserialized = list(serializers.deserialize('json', request.session.get('search_queryset')))
        pk_list = []
        for p in deserialized:
            pk_list.append(p.object.pk)
        queryset = WEC_Typ.objects.filter(pk__in=pk_list)
        for obj in queryset:
            row_num += 1
            row = [obj.manufacturer.name, obj.name, obj.output_power, obj.amount_turbine_of_type_under_contract, obj.serviced_by_dwt]
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response