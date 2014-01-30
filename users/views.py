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
