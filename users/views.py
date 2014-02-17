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

        repo_user_commits = dict()
        for commit in commits:
            commit_repos = commit.repos.all()
            for commit_repo in commit_repos:
                repo = commit_repo.repo
                if not repo_user_commits.has_key(repo):
                    repo_user_commits[repo]=list()
                repo_user_commits[repo].append(commit)


        context['repo_user_commits'] = repo_user_commits

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