import itertools
from datetime import datetime
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart

from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.text import slugify
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import WEC_Typ, Manufacturer, Image
from projects.models import Comment
from player.models import Player
from wind_farms.models import WindFarm
from turbine.models import Turbine, Contract, ServiceLocation
from projects.models import Project
from .filters import WEC_TypFilter
from .forms import WEC_TypForm, ImageForm
from projects.forms import CommentForm
from turbine.utils import TurbineSerializer, ServiceLocationSerializer, ContractSerializer, ProjectSerializer
from .utils import FilteredView

class WEC_TypList(FilteredView):
    model = WEC_Typ
    filter_class = WEC_TypFilter
    template_name = 'polls/wec_typ/list.html'

def home(request):
    wec_types = WEC_Typ.objects.filter(available=True).count()
    manufacturers = Manufacturer.objects.all().count()
    windfarms = WindFarm.objects.filter(available=True).count()
    turbines = Turbine.objects.filter(available=True).count()
    players = Player.objects.filter(available=True).count()
    users = User.objects.all().count()
    return render(request, 'polls/home.html', {'wec_types': wec_types, 'manufacturers': manufacturers, 'windfarms':windfarms, 'turbines':turbines,'players':players, 'users': users,})

def map(request):
    turbines = TurbineSerializer(Turbine.objects.filter(latitude__isnull=False, longitude__isnull=False), many=True).data
    projects = ProjectSerializer(Project.objects.filter(available=True, status__in=[_("Coffee"), _("Soft Offer"), _("Hard Offer"), _("Negotiation"), _("Final Negotiation")]).exclude(turbines=None).prefetch_related('turbines', 'turbines__wind_farm', 'turbines__wec_typ', 'turbines__wec_typ__manufacturer', 'turbines__wind_farm__country', 'turbines__owner', 'comment').select_related('customer', 'sales_manager'), many=True).data
    contracts = ContractSerializer(Contract.objects.filter(active=True).exclude(turbines=None).prefetch_related('turbines', 'turbines__wind_farm'), many=True).data
    service_locations = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True), many=True).data
    return render(request, 'polls/map.html', {'turbines': turbines, 'projects': projects, 'contracts': contracts, 'service_locations': service_locations,})

class WEC_TypCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = WEC_Typ
    form_class = WEC_TypForm
    permission_required = 'polls.add_wec_typ'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not WEC_Typ.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        redirect = super(WEC_TypCreate, self).form_valid(form)
        wec_typ_created = self.object.id
        change = Comment(text=_('created Turbine Type'), object_id=wec_typ_created, content_type=ContentType.objects.get(app_label = 'polls', model = 'wec_typ'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return redirect

class WEC_TypEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = WEC_Typ
    form_class = WEC_TypForm
    permission_required = 'polls.change_wec_typ'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.updated = datetime.now()
        change = Comment(text=_('edited Turbine Type'), object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'polls', model = 'wec_typ'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return super(WEC_TypEdit, self).form_valid(form)

class ImageCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Image
    form_class = ImageForm
    permission_required = 'polls.add_image'
    raise_exception = True

    def get_success_url(self):
        wec_typ = get_object_or_404(WEC_Typ, id=self.kwargs['wec_typ_id'])
        success_url = reverse_lazy('polls:wec_typ_detail', kwargs={'id': wec_typ.id, 'slug': wec_typ.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        images = Image.objects.all()
        wec_typ = get_object_or_404(WEC_Typ, id=self.kwargs['wec_typ_id'])
        form.instance.name = str(wec_typ.manufacturer) + " " + str(wec_typ.name) + " #" + str(len(images))
        form.instance.object_id = self.kwargs['wec_typ_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'polls', model = 'wec_typ')
        form.instance.created = datetime.now()
        return super(ImageCreate, self).form_valid(form)

def wec_typ_detail(request, id, slug):
    wec_typ = get_object_or_404(WEC_Typ, id=id, slug=slug, available=True)
    changes = wec_typ.comment.filter(text__in=[_("created Turbine Type"), _("edited Turbine Type")])
    turbines = wec_typ.turbine_of_type()
    turbines_count = turbines.count()
    serialized_turbines = TurbineSerializer(turbines.filter(latitude__isnull=False, longitude__isnull=False), many=True).data
    context = {'wec_typ': wec_typ, 'json':serialized_turbines, 'turbines_count': turbines_count, 'changes': changes}
    if not wec_typ.power_curve == None:
        power_curve_data = SimpleDataSource(data=wec_typ.get_power_curve_data())
        chart = LineChart(power_curve_data, html_id='power_curve', options = { 'title': 'Power Curve', 'subtitle': 'in MW', 'colors': ['#e2431e'], 'legend': { 'position': 'bottom' }, 'vAxis': { 'title': 'Output Power [MW]' }, 'hAxis': { 'title': 'Wind Speed [m/s]' } })
        context = {'wec_typ': wec_typ, 'chart': chart}
    return render(request, 'polls/wec_typ/detail.html', context)

class CommentCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'wec_typ.comment'
    raise_exception = True

    def get_success_url(self):
        turbine_model = get_object_or_404(WEC_Typ, id=self.kwargs['id'])
        success_url = reverse_lazy('polls:wec_typ_detail', kwargs={'id': turbine_model.id, 'slug': turbine_model.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['id']
        form.instance.content_type = ContentType.objects.get(app_label = 'polls', model = 'wec_typ')
        form.instance.created = datetime.now()
        form.instance.created_by = self.request.user
        return super(CommentCreate, self).form_valid(form)

class CommentEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'wec_typ.comment'
    raise_exception = True

    def get_success_url(self):
        turbine_model = get_object_or_404(WEC_Typ, id=self.kwargs['id'])
        success_url = reverse_lazy('polls:wec_typ_detail', kwargs={'id': turbine_model.id, 'slug': turbine_model.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['id']
        form.instance.content_type = ContentType.objects.get(app_label = 'polls', model = 'wec_typ')
        return super(CommentEdit, self).form_valid(form)

