import itertools
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.text import slugify
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Player
from .tables import PlayerTable
from .filters import PlayerListFilter
from .utils import PagedFilteredTableView
from .forms import PlayerForm

def player_detail(request, id, slug):
    player = get_object_or_404(Player, id=id, slug=slug)
    related_service = player.relatedService()
    related_dev = player.relatedDevelopers()
    related_com = player.relatedCom_operators()
    related_tec = player.relatedTec_operators()
    related_own = player.relatedOwners()
    return render(request, 'player/detail.html', {'player': player, 'relSer': related_service, 'relDev': related_dev, 'relCom': related_com, 'relTec': related_tec, 'relOwn': related_own,})

class PlayerCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = Player
    form_class = PlayerForm
    success_url = reverse_lazy('player:new_player')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not Player.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        send_mail('New Player submitted', 'Check', 'stefschroedter@gmail.de', ['s.schroedter@deutsche-windtechnik.com'])
        return super(PlayerCreate, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class PlayerEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Player
    form_class = PlayerForm
    success_url = reverse_lazy('player:player_list')

    def form_valid(self, form):
        form.instance.available = False
        form.instance.updated = datetime.now()
        return super(PlayerEdit, self).form_valid(form)

    success_message = 'Thank you! Your submit will be processed.'

class PlayerList(PagedFilteredTableView):
    model = Player
    table_class = PlayerTable
    filter_class = PlayerListFilter
