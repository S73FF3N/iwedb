from datetime import datetime
import itertools
from dal import autocomplete

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from .models import Turbine, Contract
from projects.models import Comment
from .tables import TurbineTable, ContractTable
from .filters import TurbineListFilter, ContractListFilter
from .utils import PagedFilteredTableView, ContractTableView
from .forms import TurbineForm, ContractForm
from projects.forms import CommentForm
from wind_farms.models import WindFarm, Country
from polls.models import WEC_Typ, Manufacturer
from player.models import Player, Person
from django.contrib.auth.models import User

def turbine_detail(request, id, slug):
    turbine = get_object_or_404(Turbine, id=id, slug=slug)
    return render(request, 'turbine/detail.html', {'turbine': turbine})

class TurbineCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "turbine/turbine_form.html"
    model = Turbine
    form_class = TurbineForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.slug = orig = slugify(str(form.instance.turbine_id))
        for x in itertools.count(1):
            if not Turbine.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        redirect = super(TurbineCreate, self).form_valid(form)
        turbine_created = self.object.id
        change = Comment(text='created turbine', object_id=turbine_created, content_type=ContentType.objects.get(app_label = 'turbine', model = 'turbine'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return redirect

def duplicate_turbine(request, id, slug):
    turbine = get_object_or_404(Turbine, id=id, slug=slug)
    data = {'turbine_id': turbine.turbine_id, 'wind_farm': turbine.wind_farm, 'wec_typ': turbine.wec_typ, 'hub_height': turbine.hub_height, 'commisioning': turbine.commisioning, 'dismantling': turbine.dismantling,
            'developer': turbine.developer.all(), 'asset_management': turbine.asset_management.all(), 'com_operator': turbine.com_operator.all(), 'tec_operator': turbine.tec_operator.all(), 'service': turbine.service.all(), 'owner': turbine.owner}
    form = TurbineForm(request.POST or None, request.FILES or None, initial=data)
    form.instance.available = True
    form.instance.slug = orig = slugify(str(form.instance.turbine_id))
    for x in itertools.count(1):
        if not Turbine.objects.filter(slug=form.instance.slug).exists():
            break
        form.instance.slug = '%s-%d' % (orig, x)
    form.instance.created = datetime.now()
    form.instance.updated = datetime.now()
    if request.method == "POST":
        if form.is_valid():
            turbine = form.save()
            comment = Comment(text='created turbine', object_id=turbine.id, content_type=ContentType.objects.get(app_label = 'turbine', model = 'turbine'), created=datetime.now(), created_by=request.user)
            comment.save()
            return HttpResponseRedirect(reverse_lazy('turbines:turbine_detail', kwargs={'id': turbine.id, 'slug': turbine.slug}))
    return render(request, 'turbine/turbine_form.html', {'form':form})


class TurbineEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Turbine
    form_class = TurbineForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.updated = datetime.now()
        change = Comment(text='edited turbine', object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'turbine', model = 'turbine'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return super(TurbineEdit, self).form_valid(form)

def contract_detail(request, id):
    contract = get_object_or_404(Contract, id=id)
    comments = contract.comment.all().exclude(text__in=["created contract", "edited contract"])
    changes = contract.comment.all().filter(text__in=["created contract", "edited contract"])
    return render(request, 'turbine/contract_detail.html', {'contract': contract, 'comments': comments, 'changes': changes})

class ContractCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = "turbine/contract_form.html"
    model = Contract
    form_class = ContractForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def form_valid(self, form):
        form.instance.active = True
        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        redirect = super(ContractCreate, self).form_valid(form)
        contract_created = self.object.id
        comment = Comment(text='created contract', object_id=contract_created, content_type=ContentType.objects.get(app_label = 'turbine', model = 'contract'), created=datetime.now(), created_by=self.request.user)
        comment.save()
        return redirect

class ContractEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contract
    form_class = ContractForm

    def form_valid(self, form):
        form.instance.active = True
        form.instance.updated = datetime.now()
        change = Comment(text='edited contract', object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'turbine', model = 'contract'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return super(ContractEdit, self).form_valid(form)

class CommentCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    templete_name = "projects/comment_form.html"
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def get_success_url(self):
        contract = get_object_or_404(Comment, id=self.kwargs['contract_id'])
        success_url = reverse_lazy('turbines:contract_detail', kwargs={'id': contract.id})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['contract_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'turbine', model = 'contract')
        form.instance.created = datetime.now()
        form.instance.created_by = self.request.user
        return super(CommentCreate, self).form_valid(form)

class TurbineList(PagedFilteredTableView):
    model = Turbine
    table_class = TurbineTable
    filter_class = TurbineListFilter

class ContractList(ContractTableView):
    model = Contract
    table_class = ContractTable
    filter_class = ContractListFilter

class TurbineIDAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Turbine.objects.filter(available=True)
        windfarm = self.forwarded.get('windfarm', None)

        if windfarm:
            qs = qs.filter(wind_farm__in=windfarm)

        if self.q:
            qs = qs.filter(turbine_id__istartswith=self.q)

        return qs

class WindFarmAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = WindFarm.objects.filter(available=True)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class WEC_TypAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = WEC_Typ.objects.filter(available=True)
        manufacturer = self.forwarded.get('wec_typ__manufacturer', None)
        manufacturer2 = self.forwarded.get('turbines__wec_typ__manufacturer', None)

        if manufacturer:
            qs = qs.filter(manufacturer__in=manufacturer)

        if manufacturer2:
            qs = qs.filter(manufacturer__in=manufacturer2)

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

        qs = Player.objects.filter(available=True)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Country.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Person.objects.filter(available=True)
        customer = self.forwarded.get('customer', None)

        if customer:
            qs = qs.filter(company=customer)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.filter(groups__name__in=["Sales"])

        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)

        return qs