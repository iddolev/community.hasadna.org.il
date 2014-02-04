from django.contrib import admin
from repos.models import Repo

class RepoAdmin(admin.ModelAdmin):
    exclude = ('description',)
    list_display = ('full_name',)

admin.site.register(Repo, RepoAdmin)
