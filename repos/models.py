from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class Project(models.Model):
    english_name = models.CharField(_('Project Name (English)'), unique=True, max_length=255, blank=True)
    hebrew_name = models.CharField(_('Project Name (Hebrew)'), unique=True, max_length=255, blank=True)
    description = models.TextField(_('Project Description'), blank=True)

    def __unicode__(self):
        return self.english_name

    def get_absolute_url(self):
        return reverse('repos:project_detail', kwargs={'pk': self.pk})


class ProjectOwner(models.Model):
    owner = models.ForeignKey('users.User',
                              related_name='projects',
                              blank=False,
                              null=False)
    project = models.ForeignKey('repos.Project',
                                related_name='owners',
                                blank=False,
                                null=False)

class Repo(models.Model):
    full_name = models.CharField(_('Repo full name ("username/repo_name")'), unique=True, max_length=255, blank=True)
    description = models.TextField(_('Repo description from github'), blank=True)
    last_fetch = models.DateTimeField(_('Last time commits were fetched'), auto_now=True, blank=False)
    project = models.ForeignKey('repos.Project',
                                  related_name='repos',
                                  blank=False,
                                  null=False)


class Commit(models.Model):
    author_github_username = models.CharField(_('Github username of author'),max_length=255, null=False, blank=False)
    author_name = models.CharField(_('Name of author according to github'),max_length=255, null=True, blank=True)
    author_url = models.CharField(_('Author Github page URL'), max_length=255, blank=True)
    author_email = models.CharField(_('Author email'), max_length=255, blank=True)
    author_date = models.DateTimeField(_('Author date'), blank=False)
    author = models.ForeignKey('users.User',
                                  related_name='authored_commits',
                                  blank=True,
                                  null=True,
                                  on_delete=models.SET_NULL)
    committer_github_username = models.CharField(_('Github username of committer'),max_length=255,null=False, blank=False)
    committer_name = models.CharField(_('Name of committer according to github'),max_length=255, null=True, blank=True)
    committer_url = models.CharField(_('Author Github page URL'), max_length=255, blank=True)
    committer_email = models.CharField(_('Committer email'), max_length=255, blank=True)
    committer_date = models.DateTimeField(_('Committer date'), blank=False)
    committer = models.ForeignKey('users.User',
                                     related_name='committed_commits',
                                     blank=True,
                                     null=True,
                                     on_delete=models.SET_NULL)
    sha = models.CharField(_('SHA'), max_length=255, blank=False)
    url = models.CharField(_('Commit URL'), max_length=255, blank=True)
    message = models.TextField(_('Commit message'), blank=True)
    imported_on = models.DateTimeField(_('Imported from Github on'), auto_now_add=True, blank=False)

class CommitRepo(models.Model):
    commit = models.ForeignKey('Commit', related_name='repos')
    repo = models.ForeignKey('Repo', related_name='commits')

class CommitParent(models.Model):
    child = models.ForeignKey('Commit', related_name='parents')
    parent = models.ForeignKey('Commit', related_name='children')

