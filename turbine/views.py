from datetime import datetime
import itertools

from dal import autocomplete

from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Turbine, Contract
from .tables import TurbineTable
from .filters import TurbineListFilter
from .utils import PagedFilteredTableView
from .forms import TurbineForm, ContractForm
from wind_farms.models import WindFarm, Country
from polls.models import WEC_Typ, Manufacturer
from player.models import Player

def turbine_detail(request, id, slug):
    turbine = get_object_or_404(Turbine, id=id, slug=slug)
    return render(request, 'turbine/detail.html', {'turbine': turbine})

class TurbineCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "turbine/turbine_form.html"
    login_url = 'login'
    redirect_field_name = 'next'
    model = Turbine
    form_class = TurbineForm
    success_url = reverse_lazy('turbines:new_turbine')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.slug = orig = slugify(str(form.instance.turbine_id))
        for x in itertools.count(1):
            if not Turbine.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        send_mail('New Turbine submitted', 'Check', 'stefschroedter@gmail.de', ['s.schroedter@deutsche-windtechnik.com'])
        return super(TurbineCreate, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class TurbineEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Turbine
    form_class = TurbineForm
    success_url = reverse_lazy('turbines:turbine_list')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.updated = datetime.now()
        return super(TurbineEdit, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class ContractCreate(SuccessMessageMixin, CreateView):
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy('turbines:new_contract')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        send_mail('New Contract submitted', 'Check', 'stefschroedter@gmail.de', ['s.schroedter@deutsche-windtechnik.com'])
        return super(ContractCreate, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class TurbineList(PagedFilteredTableView):
    model = Turbine
    table_class = TurbineTable
    filter_class = TurbineListFilter

class WindFarmAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = WindFarm.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class WEC_TypAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = WEC_Typ.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class ManufacturerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Manufacturer.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class ActorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Player.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class TurbineAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Turbine.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Country.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs