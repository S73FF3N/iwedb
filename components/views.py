from datetime import datetime
import itertools

from polls.models import Image
from .forms import GearboxForm, GeneratorForm, TowerForm
from polls.forms import ImageForm
from .filters import GearboxFilter, GeneratorFilter, TowerFilter
from .models import Gearbox, Generator, Tower

from django.shortcuts import render, get_object
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

def component_type_list(request):
    gearbox_form = GearboxForm()
    gearboxes = Gearbox.objects.filter(available=True)
    gearbox_filter = GearboxFilter(request.GET, queryset=gearboxes)

    generator_form = GeneratorForm()
    generators = Generator.objects.filter(available=True)
    generator_filter = GeneratorFilter(request.GET, queryset=generators)

    tower_form = TowerForm()
    towers = Tower.objects.filter(available=True)
    tower_filter = TowerFilter(request.GET, queryset=towers)
    return render(request, 'components/list.html', {'gearboxes': gearboxes, 'gearboxfilter': gearbox_filter, 'gearboxform': gearbox_form,
                                                    'generators': generators, 'generatorfilter': generator_filter, 'generatorform': generator_form,
                                                    'towers': towers, 'towerfilter': tower_filter, 'towerform': tower_form})

def gearbox_detail(request, id, slug):
    gearbox = get_object_or_404(Gearbox, id=id, slug=slug, available=True)
    return render(request, 'components/gearbox_detail.html', {'component': gearbox})

def generator_detail(request, id, slug):
    generator = get_object_or_404(Generator, id=id, slug=slug, available=True)
    return render(request, 'components/generator_detail.html', {'component': generator})

def tower_detail(request, id, slug):
    tower = get_object_or_404(Tower, id=id, slug=slug, available=True)
    return render(request, 'components/tower_detail.html', {'component': tower})

class GearboxCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = Gearbox
    form_class = GearboxForm
    success_url = reverse_lazy('components:new_gearbox')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not Gearbox.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        send_mail('New Gearbox submitted', 'Check', 'stefschroedter@gmail.de', ['s.schroedter@deutsche-windtechnik.com'])
        return super(GearboxCreate, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class GeneratorCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = Generator
    form_class = GeneratorForm
    success_url = reverse_lazy('components:new_generator')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not Generator.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        send_mail('New Generator submitted', 'Check', 'stefschroedter@gmail.de', ['s.schroedter@deutsche-windtechnik.com'])
        return super(GeneratorCreate, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class TowerCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = Tower
    form_class = TowerForm
    success_url = reverse_lazy('components:new_tower')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not Tower.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        send_mail('New Tower submitted', 'Check', 'stefschroedter@gmail.de', ['s.schroedter@deutsche-windtechnik.com'])
        return super(TowerCreate, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class GearboxEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Gearbox
    form_class = GearboxForm
    success_url = reverse_lazy('components:component_type_list')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.updated = datetime.now()
        return super(GearboxEdit, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class GeneratorEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Generator
    form_class = GeneratorForm
    success_url = reverse_lazy('components:component_type_list')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.updated = datetime.now()
        return super(GeneratorEdit, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class TowerEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tower
    form_class = TowerForm
    success_url = reverse_lazy('components:component_type_list')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.updated = datetime.now()
        return super(TowerEdit, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

#class ImageCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#    login_url = 'login'
#    redirect_field_name = 'next'
#    model = Image
#    form_class = ImageForm
#    success_url = reverse_lazy('components:component_type_list')

#    def form_valid(self, form):
#        form.instance.available = False
#        images = Image.objects.all()
#        if get_object(Gearbox, slug=self.kwargs['component_slug']):
#            component = get_object(Gearbox, slug=self.kwargs['component_slug'])
#
#        form.instance.name = str(wec_typ.manufacturer) + " " + str(wec_typ.name) + " #" + str(len(images))
#        form.instance.object_id = self.kwargs['wec_typ_id']
#        form.instance.content_type = ContentType.objects.get(app_label = 'polls', model = 'wec_typ')
#        form.instance.created = datetime.now()
#        #send_mail('New Wind Turbine Model submitted', 'Check', 'stefschroedter@gmail.de', ['s.schroedter@deutsche-windtechnik.com'])
#        return super(ImageCreate, self).form_valid(form)
#
#    success_message = 'Thank you! Your submit will be processed.'