class FilteredView():
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(FilteredView, self).get_queryset().filter(available=True)#.annotate(amount_turbines=Count('turbines'))
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(FilteredView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    return context