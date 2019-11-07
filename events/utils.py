from django_tables2 import SingleTableView

class PagedFilteredTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self,*args, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(PagedFilteredTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    return context