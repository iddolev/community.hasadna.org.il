from repos.models import Repo, Commit, CommitParent, CommitRepo
from users.models import User
from django.utils.timezone import make_aware, utc

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
        author = get_user_by_github_id_or_none(commit_from_api.author.id)
        committer = get_user_by_github_id_or_none(commit_from_api.committer.id)

        commit, created = Commit.objects.get_or_create(
            author_github_id = commit_from_api.author.id,
            author_url = commit_from_api.author.url,
            author_name = commit_from_api.commit.author.name,
            author_email = commit_from_api.commit.author.email,
            author_date = make_aware(commit_from_api.commit.author.date, utc),
            committer_github_id = commit_from_api.committer.id,
            committer_url = commit_from_api.committer.url,
            committer_name = commit_from_api.commit.committer.name,
            committer_email = commit_from_api.commit.committer.email,
            committer_date = make_aware(commit_from_api.commit.committer.date, utc),
            sha = commit_from_api.sha,
            url = commit_from_api.url,
            message = commit_from_api.commit.message,
            author = author,
            committer = committer,
        )

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
            except Commit.ObjectDoesNotExist:
                pass

def get_user_by_github_id_or_none(github_id):
        cut = User.objects.filter(github_id=github_id)
        if len(cut)!=1:
            return None
        else:
            return cut[0]
