import django_tables2 as dt2
from .models import Player

class PlayerTable(dt2.Table):
    name = dt2.LinkColumn(None)

    class Meta:
        model = Player
        fields =('name', 'country', 'city', 'postal_code', 'adress', 'phone', 'mail', 'web', 'sector')
        attrs = {"class": "windfarms"}
        per_page = 20
        empty_text = "There are no actors matching the search criteria..."