from datetime import datetime
import itertools

from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from .admin import ProjectRessources

from .models import Project, Comment
from .tables import ProjectTable
from .filters import ProjectListFilter
from .utils import PagedFilteredTableView
from .forms import ProjectForm, CommentForm, DrivingForm

class ProjectList(PagedFilteredTableView):
    model = Project
    table_class = ProjectTable
    filter_class = ProjectListFilter

    def export_xlsx(request):
        data = ProjectRessources().export()
        response = HttpResponse(data.xlsx, content_type='applications/vnd.ms-excel')
        response['Content-Disposition'] = 'attachement; filename="projects.xlsx"'
        return response

class ProjectCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "projects/project_form.html"
    login_url = 'login'
    redirect_field_name = 'next'
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.available = True
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not Project.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        redirect = super(ProjectCreate, self).form_valid(form)
        project_created = self.object.id
        comment = Comment(text='created project', object_id=project_created, content_type=ContentType.objects.get(app_label = 'projects', model = 'project'), created=datetime.now(), created_by=self.request.user)
        comment.save()
        return redirect

class ProjectEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.available = True
        form.instance.updated = datetime.now()
        comment = Comment(text='edited project', object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'projects', model = 'project'), created=datetime.now(), created_by=self.request.user)
        comment.save()
        return super(ProjectEdit, self).form_valid(form)

class CommentCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        success_url = reverse_lazy('projects:project_detail', kwargs={'id': project.id, 'slug': project.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['project_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'projects', model = 'project')
        form.instance.created = datetime.now()
        form.instance.created_by = self.request.user
        return super(CommentCreate, self).form_valid(form)

class CommentEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        success_url = reverse_lazy('projects:project_detail', kwargs={'id': project.id, 'slug': project.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['project_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'projects', model = 'project')
        return super(CommentEdit, self).form_valid(form)

def project_detail(request, id, slug):
    project = get_object_or_404(Project, id=id, slug=slug)
    comments = project.comment.all().exclude(text__in=["created project", "edited project"])
    changes = project.comment.all().filter(text__in=["created project", "edited project"])
    result = None
    if request.method == "POST":
        driving_form = DrivingForm(request.POST)
        if driving_form.is_valid():
            distance = driving_form.cleaned_data["distance"]
            hours = driving_form.cleaned_data["hours"]
            result = project.driving_rate(distance, hours)
    else:
        driving_form = DrivingForm()

    return render(request, 'projects/detail.html', {'project': project, 'comments': comments, 'changes': changes, 'form': driving_form, 'result': result})