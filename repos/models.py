from django.db import models
from django.utils.translation import ugettext_lazy as _

class Repo(models.Model):
    github_repo_id = models.IntegerField(_('Github repo id'),unique=True, null=False, blank=False)
    full_name = models.CharField(_('Repo full name'), max_length=255, blank=True)
    description = models.TextField(_('Repo description from github'), blank=True)
    last_fetch = models.DateTimeField(_('Last time commits were fetched'), auto_now=True, blank=False)

class Commit(models.Model):
    author_github_id = models.IntegerField(_('Github id of author'),null=False, blank=False)
    author_url = models.CharField(_('Author Github page URL'), max_length=255, blank=True)
    author_name = models.CharField(_('Author name'), max_length=255, blank=True)
    author_email = models.CharField(_('Author email'), max_length=255, blank=True)
    author_date = models.DateTimeField(_('Author date'), blank=False)
    author = models.ForeignKey('users.User',
                                  related_name='authored_commits',
                                  blank=True,
                                  null=True,
                                  on_delete=models.SET_NULL)
    committer_github_id = models.IntegerField(_('Committer Github page URL'),null=False, blank=False)
    committer_url = models.CharField(_('Commit URL'), max_length=255, blank=True)
    committer_name = models.CharField(_('Committer name'), max_length=255, blank=True)
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

