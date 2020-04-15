from django.http import HttpResponse

from django_tables2 import SingleTableView
#from django.utils.translation import ugettext_lazy as _

from .models import Player
from .admin import PlayerResources

class PagedFilteredTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset().filter(available=True).select_related('country').prefetch_related( 'sector')
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(PagedFilteredTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    return context

    def export_xlsx(request):
        queryset = Player.objects.all()
        data = PlayerResources().export(queryset)
        response = HttpResponse(data.xlsx, content_type='applications/vnd.ms-excel')
        response['Content-Disposition'] = 'attachement; filename="actors.xlsx"'
        return response