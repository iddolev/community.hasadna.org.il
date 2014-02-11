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
        commits = self.object.authored_commits
        context['total_commits'] = len(commits.all())
        return context
