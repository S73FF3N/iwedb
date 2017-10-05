import django_tables2 as dt2
from .models import Turbine

class TurbineTable(dt2.Table):
    name = dt2.LinkColumn(None)

    class Meta:
        model = Turbine
        fields =('id', 'wind_farm', 'wec_manufacturer', 'wec_typ', 'developer', 'owner', 'com_operator', 'tec_operator', 'service', 'status')
        attrs = {"class": "turbines"}
        per_page = 30
        empty_text = "There are no wind farms matching the search criteria..."