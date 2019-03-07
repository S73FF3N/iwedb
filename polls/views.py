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
from django.db.models import Count
from django.http import HttpResponse
from django.conf import settings

from .models import WEC_Typ, Manufacturer, Image
from projects.models import Comment
from player.models import Player
from wind_farms.models import WindFarm
from turbine.models import Turbine
from .filters import WEC_TypFilter
from .forms import WEC_TypForm, ImageForm
from turbine.utils import TurbineSerializer

def wec_typ_list(request):
    form = WEC_TypForm()
    wec_types_objects = WEC_Typ.objects.exclude(available=False).annotate(amount_turbines=Count('turbine'))
    urls = {wec_type.id : wec_type.get_absolute_url() for wec_type in wec_types_objects}
    images = {}
    images_qs = {}
    img_objects = Image.objects.filter(content_type=9, available=True)
    for img in img_objects:
        if img.object_id not in images_qs:
            images_qs[img.object_id] = img.file.url
        else:
            pass
    wec_types_id = WEC_Typ.objects.exclude(available=False).values_list('id', flat=True)
    for wec_type in wec_types_id:
        try:
            images[wec_type] = images_qs[wec_type]
        except:
            images[wec_type] = '/static/img/no_image.png'
    wec_types = WEC_Typ.objects.exclude(available=False).values('manufacturer__name', 'name', 'id', 'slug')
    amount = {w.id:w.amount_turbines for w in wec_types_objects}
    wec_typ_filter = WEC_TypFilter(request.GET, queryset=wec_types)
    filter_count = wec_typ_filter.qs.count()
    return render(request, 'polls/wec_typ/list.html', {'wec_types': wec_types, 'urls': urls, 'images': images, 'filter': wec_typ_filter, 'filter_count': filter_count, 'form': form, 'amount': amount,})

def home(request):
    wec_types = WEC_Typ.objects.filter(available=True).count()
    manufacturers = Manufacturer.objects.all().count()
    windfarms = WindFarm.objects.filter(available=True).count()
    turbines = Turbine.objects.filter(available=True).count()
    players = Player.objects.filter(available=True).count()
    users = User.objects.all().count()
    return render(request, 'polls/home.html', {'wec_types': wec_types, 'manufacturers': manufacturers, 'windfarms':windfarms, 'turbines':turbines,'players':players, 'users': users,})

def conventions(request):
    with open(settings.MEDIA_ROOT+'FAQ.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=success-map.pdf'
        return response

def howto(request):
    with open(settings.MEDIA_ROOT+'Success-Map.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=success-map.pdf'
        return response

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
        change = Comment(text='created Turbine Type', object_id=wec_typ_created, content_type=ContentType.objects.get(app_label = 'polls', model = 'wec_typ'), created=datetime.now(), created_by=self.request.user)
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
        change = Comment(text='edited Turbine Type', object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'polls', model = 'wec_typ'), created=datetime.now(), created_by=self.request.user)
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
    turbines = wec_typ.turbine_of_type()
    turbines_count = turbines.count()
    serialized_turbines = TurbineSerializer(turbines.filter(latitude__isnull=False, longitude__isnull=False), many=True).data
    context = {'wec_typ': wec_typ, 'json':serialized_turbines, 'turbines_count': turbines_count}
    if not wec_typ.power_curve == None:
        power_curve_data = SimpleDataSource(data=wec_typ.get_power_curve_data())
        chart = LineChart(power_curve_data, html_id='power_curve', options = { 'title': 'Power Curve', 'subtitle': 'in MW', 'colors': ['#e2431e'], 'legend': { 'position': 'bottom' }, 'vAxis': { 'title': 'Output Power [MW]' }, 'hAxis': { 'title': 'Wind Speed [m/s]' } })
        context = {'wec_typ': wec_typ, 'chart': chart}
    return render(request, 'polls/wec_typ/detail.html', context)

