from datetime import datetime
import itertools

from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import WindFarm
from .tables import WindFarmTable
from .filters import WindFarmListFilter
from .utils import PagedFilteredTableView
from .forms import WindFarmForm

def windfarm_detail(request, id, slug):
    windfarm = get_object_or_404(WindFarm, id=id, slug=slug, available=True)
    return render(request, 'wind_farms/detail.html', {'windfarm': windfarm})

class WindFarmCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = WindFarm
    form_class = WindFarmForm
    success_url = reverse_lazy('wind_farms:new_wind_farm')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not WindFarm.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        send_mail('New Wind Farm submitted', 'Check', 'stefschroedter@gmail.de', ['s.schroedter@deutsche-windtechnik.com'])
        return super(WindFarmCreate, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class WindFarmEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = WindFarm
    form_class = WindFarmForm
    success_url = reverse_lazy('wind_farms:new_wind_farm')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.updated = datetime.now()
        return super(WindFarmEdit, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class WindFarmList(PagedFilteredTableView):
    model = WindFarm
    table_class = WindFarmTable
    filter_class = WindFarmListFilter
