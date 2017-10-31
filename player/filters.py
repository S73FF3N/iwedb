import django_filters
from .models import Player

class PlayerListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    city = django_filters.CharFilter(lookup_expr='icontains', label='City')

    class Meta:
        model = Player
        fields = ['name', 'country', 'city', 'postal_code', 'web', 'mail', 'adress', 'sector']
        order_by = ['pk']