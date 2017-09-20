from django.shortcuts import render, get_object_or_404
from .forms import ComponentForm
from .filters import ComponentFilter
from .models import Component

def component_type_list(request):
    form = ComponentForm()

    components = Component.objects.filter(available=True)
    component_filter = ComponentFilter(request.GET, queryset=components)
    return render(request, 'components/list.html', {'components': components, 'filter': component_filter, 'form': form})

def component_detail(request, id, slug):
    component = get_object_or_404(Component, id=id, slug=slug, available=True)
    return render(request,
                  'components/detail.html',
                  {'component': component})