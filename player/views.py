import itertools
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.utils.text import slugify
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _

from .models import Player, Person, File
from projects.models import Comment
from projects.forms import CommentForm
from .tables import PlayerTable
from .filters import PlayerListFilter
from .utils import PagedFilteredTableView
from .forms import PlayerForm, PersonForm, PersonEditForm, FileForm

def player_detail(request, id, slug):
    player = get_object_or_404(Player, id=id, slug=slug)
    files = player.file.filter(available=True)
    changes = player.comment.all().filter(text__in=[_("created actor"), _("edited actor")])
    headed_organisations = player.headed_organisations()
    serviced_turbines = player.serviced_turbines()
    amount_serviced_turbines = serviced_turbines.count()
    serviced_turbines_dict = {}
    for t in serviced_turbines:
        if t.wec_typ not in serviced_turbines_dict.keys():
            serviced_turbines_dict[t.wec_typ] = [{'turbine_id': t.turbine_id, 'link': t.get_absolute_url()}]
        else:
            serviced_turbines_dict[t.wec_typ].append({'turbine_id': t.turbine_id, 'link': t.get_absolute_url()})
    developed_turbines = player.developed_turbines()
    amount_developed_turbines = developed_turbines.count()
    developed_turbines_dict = {}
    for t in developed_turbines:
        if t.wec_typ not in developed_turbines_dict.keys():
            developed_turbines_dict[t.wec_typ] = [{'turbine_id': t.turbine_id, 'link': t.get_absolute_url()}]
        else:
            developed_turbines_dict[t.wec_typ].append({'turbine_id': t.turbine_id, 'link': t.get_absolute_url()})
    asset_managed_turbines = player.asset_managed_turbines()
    amount_asset_managed_turbines = len(asset_managed_turbines)
    asset_managed_turbines_dict = {}
    for t in asset_managed_turbines:
        if t.wec_typ not in asset_managed_turbines_dict.keys():
            asset_managed_turbines_dict[t.wec_typ] = [{'turbine_id': t.turbine_id, 'link': t.get_absolute_url()}]
        else:
            asset_managed_turbines_dict[t.wec_typ].append({'turbine_id': t.turbine_id, 'link': t.get_absolute_url()})
    com_operated_turbines = player.com_operated_turbines()
    amount_com_operated_turbines = com_operated_turbines.count()
    com_operated_turbines_dict = {}
    for t in com_operated_turbines:
        if t.wec_typ not in com_operated_turbines_dict.keys():
            com_operated_turbines_dict[t.wec_typ] = [{'turbine_id': t.turbine_id, 'link': t.get_absolute_url()}]
        else:
            com_operated_turbines_dict[t.wec_typ].append({'turbine_id': t.turbine_id, 'link': t.get_absolute_url()})
    tec_operated_turbines = player.tec_operated_turbines()
    tec_operated_turbines_dict = {}
    for t in tec_operated_turbines:
        if t.wec_typ not in tec_operated_turbines_dict.keys():
            tec_operated_turbines_dict[t.wec_typ] = [{'turbine_id': t.turbine_id, 'link': t.get_absolute_url()}]
        else:
            tec_operated_turbines_dict[t.wec_typ].append({'turbine_id': t.turbine_id, 'link': t.get_absolute_url()})
    amount_tec_operated_turbines = tec_operated_turbines.count
    owned_turbines = player.owned_turbines()
    amount_owned_turbines = owned_turbines.count()
    owned_turbines_dict = {}
    for t in owned_turbines:
        if t.wec_typ not in owned_turbines_dict.keys():
            owned_turbines_dict[t.wec_typ] = [{'turbine_id': t.turbine_id, 'link': t.get_absolute_url()}]
        else:
            owned_turbines_dict[t.wec_typ].append({'turbine_id': t.turbine_id, 'link': t.get_absolute_url()})
    return render(request, 'player/detail.html', {'player': player, 'changes': changes, 'files': files, 'serviced_turbines': serviced_turbines_dict, 'amount_serviced_turbines': amount_serviced_turbines,
                                                    'headed_organisations': headed_organisations,
                                                    'developed_turbines': developed_turbines_dict, 'amount_developed_turbines': amount_developed_turbines,
                                                    'asset_managed_turbines': asset_managed_turbines_dict, 'amount_asset_managed_turbines': amount_asset_managed_turbines,
                                                    'com_operated_turbines': com_operated_turbines_dict, 'amount_com_operated_turbines': amount_com_operated_turbines,
                                                    'tec_operated_turbines': tec_operated_turbines_dict, 'amount_tec_operated_turbines': amount_tec_operated_turbines,
                                                    'owned_turbines': owned_turbines_dict, 'amount_owned_turbines': amount_owned_turbines,})

def person_detail(request, id):
    person = get_object_or_404(Person, id=id)
    changes = person.comment.all().filter(text__in=[_("created employee"), _("edited employee")])
    return render(request, 'player/person_detail.html', {'person': person, 'changes': changes,})

def sign_out_person(request, id):
    person = get_object_or_404(Person, id=id)
    person.available = False
    person.save()
    player = person.company.first()
    return player_detail(request, player.id, player.slug)

class PlayerCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = Player
    form_class = PlayerForm
    permission_required = 'player.add_player'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not Player.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        redirect_url = super(PlayerCreate, self).form_valid(form)
        player_created = self.object.id
        change = Comment(text=_('created actor'), object_id=player_created, content_type=ContentType.objects.get(app_label = 'player', model = 'player'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return redirect_url

class PlayerEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Player
    form_class = PlayerForm
    permission_required = 'player.change_player'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.updated = datetime.now()
        change = Comment(text=_('edited actor'), object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'player', model = 'player'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return super(PlayerEdit, self).form_valid(form)

def validate_actor_name(request):
    actor_name = request.POST.get('actor_name')
    view_name = request.POST.get('view_name')
    data = {
        'view_name': view_name,
        'is_taken': Player.objects.filter(name__iexact=actor_name, available=True).exists(),
        'similar_actors': list(Player.objects.filter(name__icontains=actor_name, available=True).values('name'))
        }
    return JsonResponse(data)

class PersonCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = Person
    form_class = PersonForm
    context_object_name = 'person'
    template_name = 'player/person_form.html'
    permission_required = 'player.add_person'
    raise_exception = True

    def get_success_url(self):
        player = get_object_or_404(Player, id=self.kwargs['id'])
        success_url = reverse_lazy('player:player_detail', kwargs={'id': player.id, 'slug': player.slug})
        return success_url

    def form_valid(self, form):
        new_person = form.save(commit=False)
        new_person.available = True
        new_person.created = datetime.now()
        new_person.updated = datetime.now()
        new_person.save()

        new_person.company.add(Player.objects.get(id=self.kwargs['id']))
        form.save_m2m()
        redirect_url = super(PersonCreate, self).form_valid(form)
        person_created = self.object.id
        change = Comment(text=_('created employee'), object_id=person_created, content_type=ContentType.objects.get(app_label = 'player', model = 'person'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return redirect_url

class PersonEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Person
    form_class = PersonEditForm
    context_object_name = 'person'
    template_name = 'player/person_form.html'
    permission_required = 'player.change_person'
    raise_exception = True

    def get_success_url(self):
        person = get_object_or_404(Person, id=self.kwargs['pk'])
        player = person.company.first()
        success_url = reverse_lazy('player:player_detail', kwargs={'id': player.id, 'slug': player.slug})
        return success_url

    def form_valid(self, form):
        new_person = form.save(commit=False)
        new_person.available = True
        new_person.updated = datetime.now()
        new_person.save()

        form.save_m2m()

        change = Comment(text=_('edited employee'), object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'player', model = 'person'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return super(PersonEdit, self).form_valid(form)

class PlayerList(PagedFilteredTableView):
    model = Player
    table_class = PlayerTable
    filter_class = PlayerListFilter

class FileCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = File
    form_class = FileForm
    permission_required = 'player.add_file'
    raise_exception = True

    def get_success_url(self):
        player = get_object_or_404(Player, id=self.kwargs['player_id'])
        success_url = reverse_lazy('player:player_detail', kwargs={'id': player.id, 'slug': player.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['player_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'player', model = 'player')
        form.instance.created = datetime.now()
        form.instance.created_by = self.request.user
        return super(FileCreate, self).form_valid(form)

class FileEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = File
    form_class = FileForm
    permission_required = 'player.add_file'
    raise_exception = True

    def get_success_url(self):
        player = get_object_or_404(Player, id=self.kwargs['player_id'])
        success_url = reverse_lazy('player:player_detail', kwargs={'id': player.id, 'slug': player.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['player_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'player', model = 'player')
        return super(FileEdit, self).form_valid(form)

class CommentCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'player.comment_on_person'
    raise_exception = True

    def get_success_url(self):
        if self.kwargs['model'] == 'person':
            person = get_object_or_404(Person, id=self.kwargs['id'])
            success_url = reverse_lazy('player:person_detail', kwargs={'id': person.id})
        elif self.kwargs['model'] == 'player':
            player = get_object_or_404(Player, id=self.kwargs['id'])
            success_url = reverse_lazy('player:player_detail', kwargs={'id': player.id, 'slug': player.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['id']
        if self.kwargs['model'] == 'person':
            form.instance.content_type = ContentType.objects.get(app_label = 'player', model = 'person')
        elif self.kwargs['model'] == 'player':
            form.instance.content_type = ContentType.objects.get(app_label = 'player', model = 'player')
        form.instance.created = datetime.now()
        form.instance.created_by = self.request.user
        return super(CommentCreate, self).form_valid(form)

class CommentEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'player.comment_on_person'
    raise_exception = True

    def get_success_url(self):
        if self.kwargs['model'] == 'person':
            person = get_object_or_404(Person, id=self.kwargs['id'])
            success_url = reverse_lazy('player:person_detail', kwargs={'id': person.id})
        elif self.kwargs['model'] == 'player':
            player = get_object_or_404(Player, id=self.kwargs['id'])
            success_url = reverse_lazy('player:player_detail', kwargs={'id': player.id, 'slug': player.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['id']
        if self.kwargs['model'] == 'person':
            form.instance.content_type = ContentType.objects.get(app_label = 'player', model = 'person')
        elif self.kwargs['model'] == 'player':
            form.instance.content_type = ContentType.objects.get(app_label = 'player', model = 'player')
        return super(CommentEdit, self).form_valid(form)
