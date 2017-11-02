import django_tables2 as dt2
from .models import Turbine

class TurbineTable(dt2.Table):
    turbine_id = dt2.LinkColumn(None)

    class Meta:
        model = Turbine
        fields =('turbine_id', 'wind_farm', 'wec_manufacturer', 'wec_typ', 'status')
        attrs = {"class": "windfarms"}
        per_page = 30
        empty_text = "There are no turbines matching the search criteria..."