from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from users.models import User
from forms import EditUserForm

class HomeView(ListView):
    # TODO: show users according to privacy level
    model = User


class UserView(DetailView):
    # TODO: show users according to privacy level
    model = User
    slug_field = 'nick'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        commits = self.object.authored_commits.all()
        context['total_commits'] = len(commits)

        repo_commits = dict()
        for commit in commits:
            commit_repos = commit.repos.all()
            for commit_repo in commit_repos:
                repo = commit_repo.repo
                if not repo_commits.has_key(repo):
                    repo_commits[repo]=list()
                repo_commits[repo].append(commit)

        project_repo_commits = dict()
        for repo, commits in repo_commits.items():
            project = repo.project
            if not project_repo_commits.has_key(project):
                project_repo_commits[project] = dict()
                project_repo_commits[project]['total_commits']= 0
            project_repo_commits[project][repo]=commits
            project_repo_commits[project]['total_commits'] += len(commits)

        context['project_repo_commits'] = project_repo_commits
        return context


class UserCreateView(CreateView):
    model = User
    form_class = EditUserForm
    template_name_suffix = '_create_form'

class UserUpdateView(UpdateView):
    model = User
    form_class = EditUserForm
    slug_field = 'nick'
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return self.object.get_absolute_url()