from datetime import datetime
import itertools
from dal import autocomplete
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Min, Case, When
from django.forms.formsets import formset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from .models import Turbine, Contract, Component, ComponentName, ComponentTurbineRelation
from projects.models import Comment, OfferNumber, Project, GraduatedPrice
from events.models import Event, Date
from .tables import TurbineTable, ContractTable, TerminatedContractTable, TOContractTable
from .filters import TurbineListFilter, ContractListFilter
from .utils import PagedFilteredTableView, ContractTableView
from .forms import TurbineForm, ComponentForm, BaseComponentFormSet, ContractForm, DuplicateTurbine, TerminationForm
from projects.forms import CommentForm
from wind_farms.models import WindFarm, Country
from polls.models import WEC_Typ, Manufacturer
from player.models import Player, Person
from django.contrib.auth.models import User
import logging

def turbine_detail(request, id, slug):
    turbine = get_object_or_404(Turbine, id=id, slug=slug)
    components = turbine.components.all()
    amount = None
    if request.method == "POST":
        duplicate_turbine_amount = DuplicateTurbine(request.POST, prefix="duplicate_turbine_amount")
        if duplicate_turbine_amount.is_valid():
            amount = duplicate_turbine_amount.cleaned_data["amount"]
            messages.add_message(request, messages.INFO, _("Confirm the duplication by clicking 'Go'."))
        else:
            messages.add_message(request, messages.INFO, _('Provide the amount of how often you want to duplicate the turbine.'))
            duplicate_turbine_amount = DuplicateTurbine(prefix="duplicate_turbine_amount")
    else:
        duplicate_turbine_amount = DuplicateTurbine(prefix="duplicate_turbine_amount")
    return render(request, 'turbine/detail.html', {'turbine': turbine, 'components' : components, 'form': duplicate_turbine_amount, 'amount':amount})

class TurbineCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "turbine/turbine_form.html"
    model = Turbine
    form_class = TurbineForm
    permission_required = 'turbine.add_turbine'
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
        change = Comment(text=_('created turbine'), object_id=turbine_created, content_type=ContentType.objects.get(app_label = 'turbine', model = 'turbine'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return redirect

def validate_turbine_id(request):
    turbine_id = request.POST.get('turbine_id')
    view_name = request.POST.get('view_name')
    data = {
        'view_name': view_name,
        'is_taken': Turbine.objects.filter(turbine_id__iexact=turbine_id, available=True).exists(),
        'similar_turbine_ids': list(Turbine.objects.filter(turbine_id__icontains=turbine_id, available=True).values('turbine_id'))
        }
    return JsonResponse(data)

def duplicate_turbine(request, id, slug, amount):
    turbine = get_object_or_404(Turbine, id=id, slug=slug)
    try:
        try:
            for x in range(int(amount)):
                if turbine.turbine_id[-3] == "0":
                    if turbine.turbine_id[-2] == "0":
                        if int(turbine.turbine_id[-1:])+x+1 >= 100:
                            turbine_nr = str(int(turbine.turbine_id[-1:])+x+1)
                        elif int(turbine.turbine_id[-1:])+x+1 >= 10:
                            turbine_nr = "0"+str(int(turbine.turbine_id[-1:])+x+1)
                        else:
                            turbine_nr = "00"+str(int(turbine.turbine_id[-1:])+x+1)
                    else:
                        if int(turbine.turbine_id[-2:])+x+1 >= 100:
                            turbine_nr = str(int(turbine.turbine_id[-2:])+x+1)
                        else:
                            turbine_nr = "0"+str(int(turbine.turbine_id[-2:])+x+1)
                else:
                    turbine_nr = str(int(turbine.turbine_id[-3:])+x+1)
                turbine_id = turbine.turbine_id[:-3]+turbine_nr
                slug = orig = slugify(str(turbine_id))
                for x in itertools.count(1):
                    if not Turbine.objects.filter(slug=slug).exists():
                        break
                    slug = '%s-%d' % (orig, x)
                new_turbine = Turbine(turbine_id=turbine_id, wind_farm=turbine.wind_farm, wec_typ=turbine.wec_typ, offshore=turbine.offshore, hub_height=turbine.hub_height, status=turbine.status, commisioning_year=turbine.commisioning_year, commisioning_month=turbine.commisioning_month, commisioning_day=turbine.commisioning_day, dismantling_year=turbine.dismantling_year, dismantling_month=turbine.dismantling_month, dismantling_day=turbine.dismantling_day, available=True, slug=slug, created = datetime.now(), updated = datetime.now(), owner=turbine.owner)
                new_turbine.save()
                for d in turbine.developer.all():
                    new_turbine.developer.add(d)
                for t in turbine.tec_operator.all():
                    new_turbine.tec_operator.add(t)
                for c in turbine.com_operator.all():
                    new_turbine.com_operator.add(c)
                for s in turbine.service.all():
                    new_turbine.service.add(s)
                for a in turbine.asset_management.all():
                    new_turbine.asset_management.add(a)
                comment = Comment(text=_('created turbine'), object_id=new_turbine.id, content_type=ContentType.objects.get(app_label = 'turbine', model = 'turbine'), created=datetime.now(), created_by=request.user)
                comment.save()
            return HttpResponseRedirect(reverse_lazy('wind_farms:windfarm_detail', kwargs={'id': turbine.wind_farm.id, 'slug': turbine.wind_farm.slug}))
        except:
            for x in range(int(amount)):
                if turbine.turbine_id[-2] == "0":
                    if int(turbine.turbine_id[-1:])+x+1 >= 10:
                        turbine_nr = str(int(turbine.turbine_id[-1:])+x+1)
                    else:
                        turbine_nr = "0"+str(int(turbine.turbine_id[-1:])+x+1)
                else:
                    turbine_nr = str(int(turbine.turbine_id[-2:])+x+1)
                turbine_id = turbine.turbine_id[:-2]+turbine_nr
                slug = orig = slugify(str(turbine_id))
                for x in itertools.count(1):
                    if not Turbine.objects.filter(slug=slug).exists():
                        break
                    slug = '%s-%d' % (orig, x)
                new_turbine = Turbine(turbine_id=turbine_id, wind_farm=turbine.wind_farm, wec_typ=turbine.wec_typ, offshore=turbine.offshore, hub_height=turbine.hub_height, status=turbine.status, commisioning_year=turbine.commisioning_year, commisioning_month=turbine.commisioning_month, commisioning_day=turbine.commisioning_day, dismantling_year=turbine.dismantling_year, dismantling_month=turbine.dismantling_month, dismantling_day=turbine.dismantling_day, available=True, slug=slug, created = datetime.now(), updated = datetime.now(), owner=turbine.owner)
                new_turbine.save()
                for d in turbine.developer.all():
                    new_turbine.developer.add(d)
                for t in turbine.tec_operator.all():
                    new_turbine.tec_operator.add(t)
                for c in turbine.com_operator.all():
                    new_turbine.com_operator.add(c)
                for s in turbine.service.all():
                    new_turbine.service.add(s)
                for a in turbine.asset_management.all():
                    new_turbine.asset_management.add(a)
                comment = Comment(text=_('created turbine'), object_id=new_turbine.id, content_type=ContentType.objects.get(app_label = 'turbine', model = 'turbine'), created=datetime.now(), created_by=request.user)
                comment.save()
            return HttpResponseRedirect(reverse_lazy('wind_farms:windfarm_detail', kwargs={'id': turbine.wind_farm.id, 'slug': turbine.wind_farm.slug}))
    except:
        messages.add_message(request, messages.INFO, 'Turbine could not be duplicated due to invalid turbine name.')
        return HttpResponseRedirect(reverse_lazy('turbines:turbine_detail', kwargs={'id': turbine.id, 'slug': turbine.slug}))


class TurbineEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Turbine
    form_class = TurbineForm
    permission_required = 'turbine.change_turbine'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.updated = datetime.now()
        change = Comment(text=_('edited turbine'), object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'turbine', model = 'turbine'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return super(TurbineEdit, self).form_valid(form)

def component_edit(request, turbine_id):

    turbine = get_object_or_404(Turbine, id=turbine_id)

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
    else:
        return HttpResponseRedirect(reverse_lazy('turbines:turbine_detail', kwargs={'id': turbine.id, 'slug': turbine.slug}))

    # Create the formset, specifying the form and formset we want to use.
    ComponentFormSet = formset_factory(ComponentForm, formset=BaseComponentFormSet, extra=0, can_delete=True)

    # Get our existing data.  This is used as initial data.
    component_relations = ComponentTurbineRelation.objects.filter(turbine=turbine).order_by('id_in_turbine')
    component_data = [{'component_name_verbose': component_relation.component.component_name,
                        'component_type': component_relation.component.component_type,
                        'component_manufacturer': component_relation.component.component_manufacturer,
                        'serial_nr': component_relation.serial_nr,
                        'installation_date': component_relation.installation_date,
                        'dismantling_date': component_relation.dismantling_date}
                    for component_relation in component_relations]

    if request.method == 'POST':
        component_formset = ComponentFormSet(request.POST)

        if component_formset.is_valid():

            ComponentTurbineRelation.objects.filter(turbine=turbine).delete()

            for idx, component_form in enumerate(component_formset):
                if not component_form.cleaned_data.get('DELETE'):
                    component_name_verbose = component_form.cleaned_data.get('component_name_verbose')
                    component_name_object = ComponentName.objects.get(component_name_verbose=component_name_verbose)
                    component_type = component_form.cleaned_data.get('component_type')

                    component_manufacturer = component_form.cleaned_data.get('component_manufacturer')
                    serial_nr = component_form.cleaned_data.get('serial_nr')
                    installation_date = component_form.cleaned_data.get('installation_date')
                    dismantling_date = component_form.cleaned_data.get('dismantling_date')

                    if component_name_object and component_type:
                        try:
                            component = Component.objects.get(component_name=component_name_object, component_type=component_type,component_manufacturer=component_manufacturer)
                        except ObjectDoesNotExist:
                            component = Component(component_name=component_name_object, component_type=component_type)
                            component.component_manufacturer = component_manufacturer
                            component.created_by = user
                            component.save()

                        new_component_relation = ComponentTurbineRelation(component=component, turbine=turbine)
                        new_component_relation.id_in_turbine = idx
                        new_component_relation.serial_nr = serial_nr
                        new_component_relation.installation_date = installation_date
                        new_component_relation.dismantling_date = dismantling_date
                        new_component_relation.save()

            turbine.max_component_id = len(component_formset)-1
            turbine.save()
            return HttpResponseRedirect(reverse_lazy('turbines:turbine_detail', kwargs={'id': turbine.id, 'slug': turbine.slug}))

    else:
        component_formset = ComponentFormSet(initial=component_data)

    context = {
        'component_formset': component_formset,
    }

    return render(request, 'turbine/component_form.html', context)

def contract_detail(request, id):
    contract = get_object_or_404(Contract, id=id)
    graduated_prices = contract.graduated_price.all()
    comments = contract.comment.all().exclude(text__in=[_("created contract"), _("edited contract")])
    changes = contract.comment.all().filter(text__in=[_("created contract"), _("edited contract")])
    return render(request, 'turbine/contract_detail.html', {'contract': contract, 'graduated_prices': graduated_prices, 'comments': comments, 'changes': changes})

class ContractCreate(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = "turbine/contract_form.html"
    model = Contract
    form_class = ContractForm
    permission_required = 'turbine.add_contract'
    raise_exception = True

    def form_valid(self, form):
        form.instance.active = True
        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        redirect = super(ContractCreate, self).form_valid(form)
        contract_created = self.object.id

        graduated_price_yearly_prices = self.request.POST.getlist('contract-graduated_price_yearly_price')
        form_length = len(graduated_price_yearly_prices)
        if form_length != 0:
            graduated_price_start_years = self.request.POST.getlist('contract-graduated_price_start_year')
            graduated_price_end_years = self.request.POST.getlist('contract-graduated_price_end_year')
            graduated_price_ids = self.request.POST.getlist('contract-graduated_price_id')
            graduated_price_delete = self.request.POST.getlist('contract-graduated_price_delete')

            if form_length != len(graduated_price_start_years) or form_length != len(graduated_price_end_years) or form_length != len(graduated_price_ids) or form_length != len(graduated_price_delete):
                return super(ContractCreate, self).form_invalid(form)

            for i in range(len(graduated_price_yearly_prices)):
                if graduated_price_start_years[i]=="" or graduated_price_end_years[i]=="" or graduated_price_ids[i]=="":
                    return super(ContractCreate, self).form_invalid(form)
                if graduated_price_delete[i] == "No":
                        graduated_price = GraduatedPrice(id_in_project=graduated_price_ids[i], yearly_price=graduated_price_yearly_prices[i], start_year=graduated_price_start_years[i], end_year=graduated_price_end_years[i], object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'turbine', model = 'contract'))
                        graduated_price.save()

        comment = Comment(text=_('created contract'), object_id=contract_created, content_type=ContentType.objects.get(app_label = 'turbine', model = 'contract'), created=datetime.now(), created_by=self.request.user)
        comment.save()
        return redirect

class ContractEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    permission_required = 'turbine.change_contract'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(ContractEdit, self).get_context_data(**kwargs)
        graduated_price_start_years = []
        graduated_price_end_years = []
        graduated_price_yearly_prices = []
        graduated_price_ids = []
        graduated_price_max_id = -1
        for graduated_price in self.object.graduated_price.all():
            graduated_price_start_years.append(graduated_price.start_year)
            graduated_price_end_years.append(graduated_price.end_year)
            graduated_price_yearly_prices.append(graduated_price.yearly_price)
            id_in_project = graduated_price.id_in_project
            graduated_price_ids.append(id_in_project)
            if id_in_project > graduated_price_max_id:
                graduated_price_max_id = id_in_project
        context["graduated_price_start_years"] = graduated_price_start_years
        context["graduated_price_end_years"] = graduated_price_end_years
        context["graduated_price_yearly_prices"] = graduated_price_yearly_prices
        context["graduated_price_ids"] = graduated_price_ids
        context["graduated_price_max_id"] = graduated_price_max_id
        return context

    def form_valid(self, form):
        form.instance.active = True
        form.instance.updated = datetime.now()

        graduated_price_yearly_prices = self.request.POST.getlist('contract-graduated_price_yearly_price')
        form_length = len(graduated_price_yearly_prices)
        if form_length != 0:
            graduated_price_start_years = self.request.POST.getlist('contract-graduated_price_start_year')
            graduated_price_end_years = self.request.POST.getlist('contract-graduated_price_end_year')
            graduated_price_ids = self.request.POST.getlist('contract-graduated_price_id')
            graduated_price_delete = self.request.POST.getlist('contract-graduated_price_delete')

            if form_length != len(graduated_price_start_years) or form_length != len(graduated_price_end_years) or form_length != len(graduated_price_ids) or form_length != len(graduated_price_delete):
                return super(ContractEdit, self).form_invalid(form)

            graduated_prices = self.object.graduated_price.all()
            for i in range(len(graduated_price_yearly_prices)):
                if graduated_price_start_years[i]=="" or graduated_price_end_years[i]=="" or graduated_price_ids[i]=="":
                    return super(ContractEdit, self).form_invalid(form)
                qs = graduated_prices.filter(id_in_project=graduated_price_ids[i])
                if len(qs) == 0:
                    if graduated_price_delete[i] == "No":
                        graduated_price = GraduatedPrice(id_in_project=graduated_price_ids[i], yearly_price=graduated_price_yearly_prices[i], start_year=graduated_price_start_years[i], end_year=graduated_price_end_years[i], object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'turbine', model = 'contract'))
                        graduated_price.save()
                else:
                    graduated_price = qs[0]
                    if graduated_price_delete[i] == "No":
                        graduated_price.yearly_price = graduated_price_yearly_prices[i]
                        graduated_price.start_year = graduated_price_start_years[i]
                        graduated_price.end_year = graduated_price_end_years[i]
                        graduated_price.save()
                    else:
                        graduated_price.delete()

        change = Comment(text=_('edited contract'), object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'turbine', model = 'contract'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return super(ContractEdit, self).form_valid(form)

def validate_contract_name(request):
    contract_name = request.POST.get('contract_name')
    view_name = request.POST.get('view_name')
    data = {
        'view_name': view_name,
        'is_taken': Contract.objects.filter(name__iexact=contract_name, active=True).exists(),
        'similar_contracts': list(Contract.objects.filter(name__icontains=contract_name, active=True).values('name'))
        }
    return JsonResponse(data)

class CommentCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    templete_name = "projects/comment_form.html"
    permission_required = 'turbine.can_comment_contracts'
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

class CommentEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'turbine.can_comment_contracts'
    raise_exception = True

    def get_success_url(self):
        contract = get_object_or_404(Contract, id=self.kwargs['contract_id'])
        success_url = reverse_lazy('turbines:contract_detail', kwargs={'id': contract.id})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['contract_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'turbine', model = 'contract')
        return super(CommentEdit, self).form_valid(form)

class TurbineList(PagedFilteredTableView):
    model = Turbine
    table_class = TurbineTable
    filter_class = TurbineListFilter

class ContractList(ContractTableView):
    model = Contract
    table_class = ContractTable
    filter_class = ContractListFilter

class TerminateContract(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contract
    template_name = "turbine/terminate_contract.html"
    form_class = TerminationForm
    permission_required = 'turbine.can_terminate_contract'
    raise_exception = True

    def form_valid(self, form):
        form.instance.active = False
        form.instance.updated = datetime.now()
        redirect = super(TerminateContract, self).form_valid(form)
        contract = self.object.id
        comment = Comment(text=_('terminated contract'), object_id=contract, content_type=ContentType.objects.get(app_label = 'turbine', model = 'contract'), created=datetime.now(), created_by=self.request.user)
        comment.save()
        return redirect

class TerminatedContracts(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Contract
    filterset_class = ContractListFilter
    template_name = 'turbine/terminated_contracts.html'
    table_class = TerminatedContractTable
    filter_class = ContractListFilter
    context_filter_name = 'filter'

    def get_queryset(self, *args, **kwargs):
        qs = super(TerminatedContracts, self).get_queryset().filter(active=False).prefetch_related('turbines', 'turbines__wind_farm', 'turbines__wec_typ', 'turbines__wec_typ__manufacturer').select_related('actor').annotate(first_commisioning=Case(When(turbines__commisioning_year__isnull=False, then=Min('turbines__commisioning_year'))))
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(TerminatedContracts, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context

class TOContracts(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Contract
    filterset_class = ContractListFilter
    template_name = 'turbine/to_contracts.html'
    table_class = TOContractTable
    filter_class = ContractListFilter
    context_filter_name = 'filter'

    def get_queryset(self, *args, **kwargs):
        qs = super(TOContracts, self).get_queryset().filter(technical_operation=True).prefetch_related('turbines', 'turbines__wind_farm', 'turbines__wec_typ', 'turbines__wec_typ__manufacturer').select_related('actor').annotate(first_commisioning=Case(When(turbines__commisioning_year__isnull=False, then=Min('turbines__commisioning_year'))))
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(TOContracts, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context

class TurbineIDAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        logger=logging.getLogger(__name__)
        qs = Turbine.objects.filter(available=True)
        windfarm = self.forwarded.get('windfarm', None)
        event_id = self.forwarded.get('event_id', None)

        if windfarm:
            qs = qs.filter(wind_farm__in=windfarm)

        if event_id:
            event = Event.objects.get(id=event_id)
            qs = event.turbines.all()

        if self.q:
            qs = qs.filter(turbine_id__istartswith=self.q)

        logger.info(qs)
        return qs

class ComponentNameAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = ComponentName.objects.all()

        if self.q:
            qs = qs.filter(component_name_verbose__istartswith=self.q)

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
        manufacturer3 = self.forwarded.get('manufacturer', None)

        if manufacturer:
            qs = qs.filter(manufacturer__in=manufacturer)

        if manufacturer2:
            qs = qs.filter(manufacturer__in=manufacturer2)

        if manufacturer3:
            qs = qs.filter(manufacturer__in=manufacturer3)

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
        qs = User.objects.filter(groups__name__in=["Sales", "Sales Assistant"])

        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)

        return qs

class CustomerRelationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.filter(groups__name__in=["Customer Relations", "Technical Operations"], is_active=True)

        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)

        return qs

class OfferNumberAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = OfferNumber.objects.filter()

        if self.q:
            qs = qs.filter(number__istartswith=self.q)

        return qs

class ProjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Project.objects.filter(available=True)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class EventAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Event.objects.filter()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

class DateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Date.objects.filter()

        if self.q:
            qs = qs.filter(event__icontains=self.q)

        return qs