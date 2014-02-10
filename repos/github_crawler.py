from repos.models import Repo, Commit, CommitParent, CommitRepo
from users.models import User
from django.utils.timezone import make_aware, utc
from django.core.exceptions import ObjectDoesNotExist

class GithubCrawler():
    def __init__(self, github):
        self.github = github
        self.commits_service = github.repos.commits
        self.child_parent_sha_map = dict()

    def fetch_commits_from_repo(self, repo_full_name):
        user_repo = repo_full_name.split('/')
        user = user_repo[0]
        repo = user_repo[1]
        commits = self.commits_service.list(user=user, repo=repo)
        return commits.all()


    def process_all_repos(self):
        for repo in Repo.objects.all():
            commits = self.fetch_commits_from_repo(repo.full_name)
            for commit in commits:
                self.process_repo_commit_pair(repo,commit)
        self.link_children_and_parents()

    def process_repo_commit_pair(self, repo, commit_from_api):
        # add the commit if it does not exist
        author_github_username = commit_from_api.author.login
        committer_github_username = commit_from_api.committer.login
        author = get_user_by_github_username_or_none(author_github_username)
        committer = get_user_by_github_username_or_none(committer_github_username)

        commit, created = Commit.objects.get_or_create(sha=commit_from_api.sha,
                                                       author_date=make_aware(commit_from_api.commit.author.date,
                                                                              utc),
                                                       committer_date=make_aware(commit_from_api.commit.committer.date,
                                                                                 utc))
        commit.author_github_username = author_github_username
        commit.author_url = commit_from_api.author.url
        commit.author_name = commit_from_api.commit.author.name
        commit.author_email = commit_from_api.commit.author.email
        commit.committer_url = commit_from_api.committer.url
        commit.committer_github_username = committer_github_username
        commit.committer_name = commit_from_api.commit.committer.name
        commit.committer_email = commit_from_api.commit.committer.email
        commit.sha = commit_from_api.sha
        commit.url = commit_from_api.url
        commit.message = commit_from_api.commit.message
        commit.author = author
        commit.committer = committer
        commit.save()

        # map this commit to this repo
        CommitRepo.objects.get_or_create(commit=commit,repo=repo)

        # keep map of parent-child relationships
        for parent in commit_from_api.parents:
            self.child_parent_sha_map[commit.sha] = parent.sha

    def link_children_and_parents(self):
        for child_sha, parent_sha in self.child_parent_sha_map.iteritems():
            try:
                child = Commit.objects.get(sha=child_sha)
                parent = Commit.objects.get(sha=parent_sha)
                CommitParent.objects.get_or_create(child=child,parent=parent)
            except ObjectDoesNotExist:
                pass

def get_user_by_github_username_or_none(github_username):
        cut = User.objects.filter(github_username=github_username)
        if len(cut)!=1:
            return None
        else:
            return cut[0]
