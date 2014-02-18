from django.views.generic import CreateView, DetailView, ListView, UpdateView
from repos.models import Project, Repo
from forms import EditProjectForm, AddRepoToProject
from django.http import HttpResponseRedirect

class HomeView(ListView):
    model = Project


class ProjectView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        repos = self.object.repos.all()
        repo_commits = dict()
        for repo in repos:
            commit_repos = repo.commits.all()
            commits = [commitRepo.commit for commitRepo in commit_repos]
            repo_commits[repo]=commits
        context['repo_commits'] = repo_commits
        context['repo_form'] = AddRepoToProject(self.object.pk, self.request.POST)
        return context


class ProjectCreateView(CreateView):
    model = Project
    form_class = EditProjectForm
    template_name_suffix = '_create_form'


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = EditProjectForm
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return self.object.get_absolute_url()


def add_repo(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = AddRepoToProject(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            repo_name = form.cleaned_data['full_name']
            project = Project.objects.get(pk=pk)
            repo = project.repos.get_or_create(full_name=repo_name, project=project)
            return HttpResponseRedirect(project.get_absolute_url()) # Redirect after POST


def remove_repo(request):
    if request.method == 'POST':
        repo_pk = request.POST['repo']
        repo = Repo.objects.get(pk=repo_pk)
        project = repo.project
        repo.delete()
        return HttpResponseRedirect(project.get_absolute_url()) # Redirect after POST
