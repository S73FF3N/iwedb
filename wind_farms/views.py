from datetime import datetime
from itertools import count, chain
import json
import urllib
import unicodedata

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import Q

from .models import WindFarm
from projects.models import Comment
from .tables import WindFarmTable
from .filters import WindFarmListFilter
from .utils import PagedFilteredTableView
from turbine.utils import TurbineSerializer
from .forms import WindFarmForm
from .models import Country

def windfarm_detail(request, id, slug):
    windfarm = get_object_or_404(WindFarm, id=id, slug=slug, available=True)
    windfarm_turbines = TurbineSerializer(windfarm.turbines().filter(latitude__isnull=False, longitude__isnull=False, status="in production"), many=True).data
    projects = []
    for t in windfarm.turbines():
        t_projects = t.relProjects()
        for p in t_projects:
            if p not in projects:
                projects.append(p)
    contracts = []
    for t in windfarm.turbines():
        t_contracts = t.relContracts()
        for c in t_contracts:
            if c not in contracts:
                contracts.append(c)
    return render(request, 'wind_farms/detail.html', {'windfarm': windfarm, 'json_turbines': windfarm_turbines, 'projects': projects, 'contracts': contracts})

class WindFarmCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = WindFarm
    form_class = WindFarmForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def form_valid(self, form):
        try:
            country = Country.objects.get(id=form['country'].value())
            country = country.name.replace(" ", "+")
            country = unicodedata.normalize('NFKD', country).encode('ascii','ignore').decode('utf-8')
            city = form['city'].value().replace(" ", "+")
            city = unicodedata.normalize('NFKD', city).encode('ascii','ignore').decode('utf-8')
            postal_code = form['postal_code'].value()
            address = "+".join((postal_code, city, country))
            link = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key=AIzaSyBPf2vVr8toXpXJ2TLInDRjWS4cLQ5tzAk"
            results = json.loads(urllib.request.urlopen(link).read().decode('utf-8'))
            first_result = results['results'][0]
            form.instance.latitude = first_result['geometry']['location']['lat']
            form.instance.longitude = first_result['geometry']['location']['lng']
        except:
            form.instance.latitude = 51.45878
            form.instance.longitude = 6.51999
        form.instance.available = True
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in count(1):
            if not WindFarm.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        redirect = super(WindFarmCreate, self).form_valid(form)
        windfarm_created = self.object.id
        change = Comment(text='created windfarm', object_id=windfarm_created, content_type=ContentType.objects.get(app_label = 'wind_farms', model = 'windfarm'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return redirect

class WindFarmEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = WindFarm
    form_class = WindFarmForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.updated = datetime.now()
        change = Comment(text='edited windfarm', object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'wind_farms', model = 'windfarm'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return super(WindFarmEdit, self).form_valid(form)

def validate_windfarm_name(request):
    windfarm_name = request.POST.get('windfarm_name')
    windfarm_second_name = request.POST.get('windfarm_second_name')
    windfarm_city = request.POST.get('windfarm_city')
    if windfarm_second_name != None and windfarm_second_name != "" and windfarm_city != None and windfarm_city != "":
        similar_windfarms = WindFarm.objects.filter(Q(name__icontains=windfarm_name, available=True) | Q(name__icontains=windfarm_second_name, available=True) | Q(name__icontains=windfarm_city, available=True)).values('name')
        similar_windfarms = similar_windfarms | WindFarm.objects.filter(Q(second_name__icontains=windfarm_name, available=True) | Q(second_name__icontains=windfarm_second_name, available=True) | Q(second_name__icontains=windfarm_city, available=True)).values('name')
        similar_windfarms = similar_windfarms | WindFarm.objects.filter(Q(city__icontains=windfarm_name, available=True) | Q(city__icontains=windfarm_second_name, available=True) | Q(city__icontains=windfarm_city, available=True)).values('name')
        similar_windfarms = chain(similar_windfarms.distinct())
    elif (windfarm_second_name == None or windfarm_second_name == "") and windfarm_city != None and windfarm_city != "":
        similar_windfarms = WindFarm.objects.filter(Q(name__icontains=windfarm_name, available=True) | Q(name__icontains=windfarm_city, available=True)).values('name')
        similar_windfarms = similar_windfarms | WindFarm.objects.filter(Q(second_name__icontains=windfarm_name, available=True) | Q(second_name__icontains=windfarm_city, available=True)).values('name')
        similar_windfarms = similar_windfarms | WindFarm.objects.filter(Q(city__icontains=windfarm_name, available=True) | Q(city__icontains=windfarm_city, available=True)).values('name')
        similar_windfarms = chain(similar_windfarms.distinct())
    elif windfarm_second_name != None and windfarm_second_name != "" and (windfarm_city == None or windfarm_city == ""):
        similar_windfarms = WindFarm.objects.filter(Q(name__icontains=windfarm_name, available=True) | Q(name__icontains=windfarm_second_name, available=True)).values('name')
        similar_windfarms = similar_windfarms | WindFarm.objects.filter(Q(second_name__icontains=windfarm_name, available=True) | Q(second_name__icontains=windfarm_second_name, available=True)).values('name')
        similar_windfarms = similar_windfarms | WindFarm.objects.filter(Q(city__icontains=windfarm_name, available=True) | Q(city__icontains=windfarm_second_name, available=True)).values('name')
        similar_windfarms = chain(similar_windfarms.distinct())
    else:
        similar_windfarms = WindFarm.objects.filter(Q(name__icontains=windfarm_name, available=True)).values('name')
        similar_windfarms = similar_windfarms | WindFarm.objects.filter(Q(second_name__icontains=windfarm_name, available=True)).values('name')
        similar_windfarms = similar_windfarms | WindFarm.objects.filter(Q(city__icontains=windfarm_name, available=True)).values('name')
        similar_windfarms = chain(similar_windfarms.distinct())
    data = {
        'is_taken': WindFarm.objects.filter(name__iexact=windfarm_name).exists(),
        'similar_windfarms': list(similar_windfarms)
        }
    return JsonResponse(data)

"""elif (windfarm_second_name == None or windfarm_second_name == "") and (windfarm_city == None or windfarm_city == ""):
        similar_windfarms = WindFarm.objects.filter(Q(name__icontains=windfarm_name, available=True)).values('name')
        similar_windfarms = similar_windfarms | WindFarm.objects.filter(Q(second_name__icontains=windfarm_name, available=True)).values('name')
        similar_windfarms = similar_windfarms | WindFarm.objects.filter(Q(city__icontains=windfarm_name, available=True)).values('name')
        similar_windfarms = chain(similar_windfarms.distinct())"""

class WindFarmList(PagedFilteredTableView):
    model = WindFarm
    table_class = WindFarmTable
    filter_class = WindFarmListFilter
