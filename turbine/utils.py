from django_tables2 import SingleTableView

import serpy
from .models import ServiceLocation

class TurbineSerializer(serpy.Serializer):
    pk = serpy.IntField()
    slug = serpy.Field()
    latitude = serpy.Field()
    longitude = serpy.Field()
    turbine_id = serpy.Field()

class ContractSerializer(serpy.Serializer):
    pk = serpy.IntField()
    name = serpy.Field()
    wind_farm = serpy.MethodField()
    latitude = serpy.MethodField()
    longitude = serpy.MethodField()

    def  get_wind_farm(self, contract):
        wind_farm = contract.turbines.all()[0].wind_farm.name
        return wind_farm

    def get_longitude(self, contract):
        turbines = contract.turbines.all().filter(latitude__isnull=False, longitude__isnull=False)
        if not turbines:
            longitude = turbines[0].windfarm.longitude
        else:
            longitude = turbines[0].longitude
        return longitude

    def get_latitude(self, contract):
        turbines = contract.turbines.all().filter(latitude__isnull=False, longitude__isnull=False)
        if not turbines:
            latitude = turbines[0].windfarm.latitude
        else:
            latitude = turbines[0].latitude
        return latitude

class ServiceLocationSerializer(serpy.Serializer):
    name = serpy.Field()
    dwt = serpy.Field()
    location_type = serpy.Field()
    latitude = serpy.Field()
    longitude = serpy.Field()

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
	    turbines = TurbineSerializer(self.filter.qs.filter(latitude__isnull=False, longitude__isnull=False), many=True).data
	    context["json"] = turbines
	    return context

class ContractTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(ContractTableView, self).get_queryset().filter(active=True)
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(ContractTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    contracts = ContractSerializer(self.filter.qs.filter(active=True), many=True).data
	    context["json"] = contracts
	    service_locations = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True), many=True).data
	    context["service_locations"] = service_locations
	    return context