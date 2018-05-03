import itertools
from datetime import datetime
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart

from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.text import slugify
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.contrib.auth.models import User

from .models import WEC_Typ, Manufacturer, Image
from player.models import Player
from wind_farms.models import WindFarm
from turbine.models import Turbine
from .filters import WEC_TypFilter
from .forms import WEC_TypForm, ImageForm

def wec_typ_list(request):
    form = WEC_TypForm()
    urls = {}
    images = {}
    for wec_type in WEC_Typ.objects.exclude(available=False):
        urls[wec_type.id]=wec_type.get_absolute_url()
    images_qs = {}
    for img in Image.objects.filter(content_type=9, available=True):
        if img.object_id not in images_qs:
            images_qs[img.object_id] = img.file.url
        else:
            pass
    for wec_type in WEC_Typ.objects.filter(available=True).values_list('id', flat=True):
        try:
            images[wec_type] = images_qs[wec_type]
        except:
            images[wec_type] = '/static/img/no_image.png'
    wec_types = WEC_Typ.objects.exclude(available=False).values('manufacturer__name', 'name', 'id', 'slug')
    wec_typ_filter = WEC_TypFilter(request.GET, queryset=wec_types)
    filter_count = wec_typ_filter.qs.count()
    return render(request, 'polls/wec_typ/list.html', {'wec_types': wec_types, 'urls': urls, 'images': images, 'filter': wec_typ_filter, 'filter_count': filter_count, 'form': form})

def home(request):
    wec_types = WEC_Typ.objects.filter(available=True).count()
    manufacturers = Manufacturer.objects.all().count()
    windfarms = WindFarm.objects.filter(available=True).count()
    turbines = Turbine.objects.filter(available=True).count()
    players = Player.objects.filter(available=True).count()
    users = User.objects.all().count()
    return render(request, 'polls/home.html', {'wec_types': wec_types, 'manufacturers': manufacturers, 'windfarms':windfarms, 'turbines':turbines,'players':players, 'users': users,})

def conventions(request):
    return render(request, 'polls/conventions.html')

class WEC_TypCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = WEC_Typ
    form_class = WEC_TypForm
    success_url = reverse_lazy('polls:new_wec_typ')

    def form_valid(self, form):
        # if admin status -> available = True
        form.instance.available = False
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not WEC_Typ.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        send_mail('New Wind Turbine Model submitted', 'Check', 'stefschroedter@gmail.de', ['s.schroedter@deutsche-windtechnik.com'])
        return super(WEC_TypCreate, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class WEC_TypEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView): #permission required
    model = WEC_Typ
    form_class = WEC_TypForm
    success_url = reverse_lazy('polls:wec_typ_filter_list')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.updated = datetime.now()
        return super(WEC_TypEdit, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class ImageCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = Image
    form_class = ImageForm
    success_url = reverse_lazy('polls:wec_typ_filter_list')

    def form_valid(self, form):
        form.instance.available = False
        images = Image.objects.all()
        wec_typ = get_object_or_404(WEC_Typ, id=self.kwargs['wec_typ_id'])
        form.instance.name = str(wec_typ.manufacturer) + " " + str(wec_typ.name) + " #" + str(len(images))
        form.instance.object_id = self.kwargs['wec_typ_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'polls', model = 'wec_typ')
        form.instance.created = datetime.now()
        #send_mail('New Wind Turbine Model submitted', 'Check', 'stefschroedter@gmail.de', ['s.schroedter@deutsche-windtechnik.com'])
        return super(ImageCreate, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

def wec_typ_detail(request, id, slug):
    wec_typ = get_object_or_404(WEC_Typ, id=id, slug=slug, available=True)
    turbines = wec_typ.turbine_of_type()
    turbines_count = turbines.count()
    serialized_turbines = serializers.serialize("json", turbines, fields=('pk', 'slug', 'latitude', 'longitude', 'turbine_id'))
    context = {'wec_typ': wec_typ, 'json':serialized_turbines, 'turbines_count': turbines_count}
    if not wec_typ.power_curve == None:
        power_curve_data = SimpleDataSource(data=wec_typ.get_power_curve_data())
        chart = LineChart(power_curve_data, html_id='power_curve', options = { 'title': 'Power Curve', 'subtitle': 'in MW', 'colors': ['#e2431e'], 'legend': { 'position': 'bottom' }, 'vAxis': { 'title': 'Output Power [MW]' }, 'hAxis': { 'title': 'Wind Speed [m/s]' } })
        context = {'wec_typ': wec_typ, 'chart': chart}
    return render(request, 'polls/wec_typ/detail.html', context)

