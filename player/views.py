import itertools
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.utils.text import slugify
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType

from .models import Player, Person
from projects.models import Comment
from projects.forms import CommentForm
from .tables import PlayerTable
from .filters import PlayerListFilter
from .utils import PagedFilteredTableView
from .forms import PlayerForm, PersonForm, PersonEditForm

def player_detail(request, id, slug):
    player = get_object_or_404(Player, id=id, slug=slug)
    related_service = player.relatedService()
    relSer_len = related_service.count()
    related_dev = player.relatedDevelopers()
    relDev_len = related_dev.count()
    related_ass = player.relatedAsset_Management()
    relAss_len = related_ass.count()
    related_com = player.relatedCom_operators()
    relCom_len = related_com.count()
    related_tec = player.relatedTec_operators()
    relTec_len = related_tec.count
    related_own = player.relatedOwners()
    relOwn_len = related_own.count()
    return render(request, 'player/detail.html', {'player': player, 'relSer': related_service, 'relSer_len': relSer_len, 'relDev': related_dev, 'relDev_len': relDev_len, 'relAss': related_ass, 'relAss_len': relAss_len,
                                                    'relCom': related_com, 'relCom_len': relCom_len, 'relTec': related_tec, 'relTec_len': relTec_len, 'relOwn': related_own, 'relOwn_len': relOwn_len,})

def person_detail(request, id):
    person = get_object_or_404(Person, id=id)
    return render(request, 'player/person_detail.html', {'person': person,})

class PlayerCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = Player
    form_class = PlayerForm
    permission_required = 'projects.has_sales_status'
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
        change = Comment(text='created actor', object_id=player_created, content_type=ContentType.objects.get(app_label = 'player', model = 'player'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return redirect_url

class PlayerEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Player
    form_class = PlayerForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.updated = datetime.now()
        change = Comment(text='edited actor', object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'player', model = 'player'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return super(PlayerEdit, self).form_valid(form)

class PersonCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = Person
    form_class = PersonForm
    context_object_name = 'person'
    template_name = 'player/person_form.html'
    permission_required = 'projects.has_sales_status'
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
        change = Comment(text='created employee', object_id=person_created, content_type=ContentType.objects.get(app_label = 'player', model = 'person'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return redirect_url

class PersonEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Person
    form_class = PersonEditForm
    context_object_name = 'person'
    template_name = 'player/person_form.html'
    permission_required = 'projects.has_sales_status'
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

        change = Comment(text='edited employee', object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'player', model = 'person'), created=datetime.now(), created_by=self.request.user)
        change.save()
        return super(PersonEdit, self).form_valid(form)

class PlayerList(PagedFilteredTableView):
    model = Player
    table_class = PlayerTable
    filter_class = PlayerListFilter

class CommentCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def get_success_url(self):
        person = get_object_or_404(Person, id=self.kwargs['person_id'])
        success_url = reverse_lazy('player:person_detail', kwargs={'id': person.id})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['person_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'player', model = 'person')
        form.instance.created = datetime.now()
        form.instance.created_by = self.request.user
        return super(CommentCreate, self).form_valid(form)

class CommentEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def get_success_url(self):
        person = get_object_or_404(Person, id=self.kwargs['person_id'])
        success_url = reverse_lazy('player:person_detail', kwargs={'id': person.id})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['person_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'player', model = 'person')
        return super(CommentEdit, self).form_valid(form)
