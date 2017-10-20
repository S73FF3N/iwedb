from datetime import datetime
import itertools

from django.shortcuts import render, get_object_or_404
from .forms import ComponentForm
from .filters import ComponentFilter
from .models import Component

from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.utils.text import slugify
from django.views.generic.edit import CreateView

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

class ComponentCreate(SuccessMessageMixin, CreateView):
    model = Component
    form_class = ComponentForm
    success_url = reverse_lazy('components:new_component')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not Component.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        send_mail('New Component submitted', 'Check', 'stefschroedter@gmail.de', ['s.schroedter@deutsche-windtechnik.com'])
        return super(ComponentCreate, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'