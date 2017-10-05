import itertools
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.utils.text import slugify
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail

from .models import Player
from .tables import PlayerTable
from .filters import PlayerListFilter
from .utils import PagedFilteredTableView
from .forms import PlayerForm

def player_detail(request, id, slug):
    player = get_object_or_404(Player, id=id, slug=slug, available=True)
    return render(request,
                  'player/detail.html',
                  {'player': player})

class PlayerCreate(SuccessMessageMixin, CreateView):
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

class PlayerList(PagedFilteredTableView):
    model = Player
    table_class = PlayerTable
    filter_class = PlayerListFilter
