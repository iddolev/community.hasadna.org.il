from django.contrib import admin
from repos.models import Repo, Project

class RepoAdmin(admin.ModelAdmin):
    exclude = ('description',)
    list_display = ('full_name',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('english_name',)

admin.site.register(Repo, RepoAdmin)
admin.site.register(Project, ProjectAdmin)
