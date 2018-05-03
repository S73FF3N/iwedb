from django_tables2 import SingleTableView

import serpy

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
        qs = super(PagedFilteredTableView, self).get_queryset().filter(available=True)
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(PagedFilteredTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    windfarms = WindFarmSerializer(self.filter.qs.filter(latitude__isnull=False, longitude__isnull=False), many=True).data
	    context["json"] = windfarms
	    return context