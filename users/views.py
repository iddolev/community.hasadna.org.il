from django.shortcuts import render
from django.views.generic import ListView, DetailView
from users.models import User


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
