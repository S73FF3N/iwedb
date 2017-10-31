from datetime import datetime
import itertools

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

def turbine_detail(request, id, slug):
    turbine = get_object_or_404(Turbine, id=id, slug=slug, available=True)
    return render(request, 'turbine/detail.html', {'turbine': turbine})

class TurbineCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "turbine/turbine_form.html"
    login_url = 'login'
    redirect_field_name = 'next'
    model = Turbine
    form_class = TurbineForm
    success_url = reverse_lazy('turbine:new_turbine')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.slug = orig = slugify(str(form.instance.name))
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
    success_url = reverse_lazy('turbines:new_turbine')

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
