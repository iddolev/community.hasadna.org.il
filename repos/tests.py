from django.db import IntegrityError, transaction
from django.test import TestCase
from users.models import User
from repos.models import Repo, Commit, CommitParent, CommitRepo
from django.utils import timezone
from github_crawler import GithubCrawler, get_user_by_github_username_or_none
from pygithub3 import Github
from mock_github import MockGithub, MockCommit

class NoGit(TestCase):
    def test_create_repo(self):
        self.assertEquals(0,Repo.objects.count())
        r = Repo.objects.create(full_name='foo/bar', description='baz')
        self.assertEquals(1, Repo.objects.count())
        with transaction.atomic():
            with self.assertRaises(Exception):
                Repo.objects.create(full_name='foo/bar', description='baz')
        self.assertEquals(1, Repo.objects.count())

    def test_create_commit_no_user(self):
        self.assertEquals(0,Commit.objects.count())
        c = Commit.objects.create(
            author_github_username='foo',
            author_date=timezone.now(),
            committer_github_username = 'bar',
            committer_date=timezone.now(),
            sha='xxx',
            message='best commit ever!'
        )
        self.assertEquals(1, Commit.objects.count())

    def test_create_commit_with_user(self):
        u = User.objects.create_user('foo', 'foo@gmail.com', 'secret')
        self.assertEquals(0,Commit.objects.count())
        c = Commit.objects.create(
            author=u,
            author_github_username='foo',
            author_date = timezone.now(),
            committer=u,
            committer_github_username = 'foo',
            committer_date = timezone.now(),
            sha='xxx',
            message='best commit ever!'
        )
        self.assertEquals(1, Commit.objects.count())

    def test_connect(self):
        u = User.objects.create_user('foo', 'foo@gmail.com', 'secret')
        r = Repo.objects.create(full_name='foo/bar', description='baz')
        c1 = Commit.objects.create(
            author=u,
            author_github_username='foo',
            author_date = timezone.now(),
            committer=u,
            committer_github_username = 'foo',
            committer_date = timezone.now(),
            sha='xxx',
            message='best commit ever!'
        )
        c1.repos.create(repo=r,commit=c1)
        self.assertEquals(r, c1.repos.all()[0].repo)
        self.assertEquals(c1, r.commits.all()[0].commit)

        c2 = Commit.objects.create(
            author=u,
            author_github_username='foo',
            author_date = timezone.now(),
            committer=u,
            committer_github_username = 'foo',
            committer_date = timezone.now(),
            sha='yyy',
            message='Even better commit!'
        )
        c2.repos.create(repo=r)
        self.assertEquals(1, len(c1.repos.all()))
        self.assertEquals(1, len(c2.repos.all()))
        self.assertEquals(2, len(r.commits.all()))
        c2.children.create(child=c1)
        self.assertEquals(1, len(c1.parents.all()))
        self.assertEquals(0, len(c1.children.all()))
        self.assertEquals(0, len(c2.parents.all()))
        self.assertEquals(1, len(c2.children.all()))
        self.assertEquals(c1, c2.children.all()[0].child)
        self.assertEquals(c2, c1.parents.all()[0].parent)

    def test_match_author_to_user(self):
        u = User.objects.create_user('foo', 'foo@gmail.com', 'secret',github_username='foo')
        known_github_username = 'foo'
        unknown_github_username = 'bar'

        matched_author = get_user_by_github_username_or_none(known_github_username)
        matched_committer = get_user_by_github_username_or_none(known_github_username)

        matched_commit = Commit.objects.create(
            author=matched_author,
            author_github_username='foo',
            author_date=timezone.now(),
            committer=matched_committer,
            committer_github_username='foo',
            committer_date=timezone.now(),
            sha='xxx',
            message='best commit ever!'
        )

        unmatched_author = get_user_by_github_username_or_none(unknown_github_username)
        unmatched_committer = get_user_by_github_username_or_none(unknown_github_username)

        matched_commit = Commit.objects.create(
            author=unmatched_author,
            author_github_username='foo',
            author_date=timezone.now(),
            committer=unmatched_committer,
            committer_github_username='foo',
            committer_date=timezone.now(),
            sha='xxx',
            message='best commit ever!'
        )


class WithGithub(TestCase):
    def test_fetch_commits_from_repo(self):
        github = Github(login='', password='')
        ghc = GithubCrawler(github)
        commits = ghc.fetch_commits_from_repo('omridor/TestForCommunity')

    def test_process_all_repos(self):
        github = Github(login='', password='')
        ghc = GithubCrawler(github)
        repo_full_name = 'omridor/TestForCommunity'
        r = Repo.objects.create(full_name=repo_full_name, description='blablabla')

        #run the script to import all commits
        ghc.process_all_repos()

        # retrieve the only repo
        self.assertEquals(1, len(Repo.objects.all()))
        r = Repo.objects.all()[0]
        self.assertEquals(repo_full_name, r.full_name)

        # get its commits
        commits = [commitRepo.commit for commitRepo in r.commits.all()]
        self.assertEquals(2, len(commits))

        #check parenthood
        commits.sort(key=lambda c: c.author_date)
        self.assertEquals(0, len(commits[0].parents.all()))
        self.assertEquals(1, len(commits[0].children.all()))
        self.assertEquals(1, len(commits[1].parents.all()))
        self.assertEquals(0, len(commits[1].children.all()))

        self.assertEquals(commits[1], commits[0].children.all()[0].child)
        self.assertEquals(commits[0], commits[1].parents.all()[0].parent)

    def test_user_matching(self):
        github = Github(login='', password='')
        ghc = GithubCrawler(github)
        repo_full_name = 'omridor/TestForCommunity'
        r = Repo.objects.create(full_name=repo_full_name, description='blablabla')
        u = User.objects.create_user(nick='foo', email='foo@gmail.com', password='secret', github_username='omridor')

        #run the script to import all commits
        ghc.process_all_repos()

        # retrieve the only repo
        self.assertEquals(1, len(Repo.objects.all()))
        r = Repo.objects.all()[0]
        self.assertEquals(repo_full_name, r.full_name)

        # get omri's commits
        commits = [commitRepo.commit for commitRepo in r.commits.filter(commit__author_github_username='omridor')]
        self.assertLess(0, len(commits))
        print commits[0].author_github_username

        #check that they point to omri's user
        for commit in commits:
            self.assertTrue(commit.author == u)
            self.assertIn(commit,u.authored_commits.all())

class MockGitHub(TestCase):
    def test_mock_seperation(self):
        gh = MockGithub()
        gh.add_mock_commit('user1','repo1',MockCommit(sha='xxx',author_username='foo'))
        gh.add_mock_commit('user1','repo2',MockCommit(sha='yyy',author_username='foo'))
        gh.add_mock_commit('user2','repo1',MockCommit(sha='zzz',author_username='foo'))
        gh.add_mock_commit('user2','repo2',MockCommit(sha='www',author_username='foo'))

        gh.add_mock_commit('user1','repo1',MockCommit(sha='aaa',author_username='foo'))
        gh.add_mock_commit('user1','repo1',MockCommit(sha='bbb',author_username='foo'))
        gh.add_mock_commit('user1','repo1',MockCommit(sha='ccc',author_username='foo'))

        self.assertEquals(4, len(gh.repos.commits.list('user1','repo1')))
        self.assertEquals(1, len(gh.repos.commits.list('user1','repo2')))
        self.assertEquals(1, len(gh.repos.commits.list('user2','repo1')))
        self.assertEquals(1, len(gh.repos.commits.list('user2','repo2')))

    def test_fetch_commits_from_repo(self):
        github = MockGithub()
        ghc = GithubCrawler(github)
        github.add_mock_commit('user1','repo1',MockCommit(sha='xxx',author_username='foo'))
        commits = ghc.fetch_commits_from_repo('user1/repo1')

    def test_process_all_repos(self):
        github = MockGithub()
        github.add_mock_commit('user1','repo1',MockCommit(sha='bbb',
                                                          author_username='foo'))
        github.add_mock_commit('user1','repo1',MockCommit(sha='aaa',
                                                          parent_shas=['bbb'],
                                                          author_username='foo'))

        ghc = GithubCrawler(github)
        repo_full_name = 'user1/repo1'
        r = Repo.objects.create(full_name=repo_full_name, description='blablabla')

        #run the script to import all commits
        ghc.process_all_repos()

        # retrieve the only repo
        self.assertEquals(1, len(Repo.objects.all()))
        r = Repo.objects.all()[0]
        self.assertEquals(repo_full_name, r.full_name)

        # get its commits
        commits = [commitRepo.commit for commitRepo in r.commits.all()]
        self.assertEquals(2, len(commits))

        #check parenthood
        commits.sort(key=lambda c: c.author_date)
        self.assertEquals(0, len(commits[0].parents.all()))
        self.assertEquals(1, len(commits[0].children.all()))
        self.assertEquals(1, len(commits[1].parents.all()))
        self.assertEquals(0, len(commits[1].children.all()))

        self.assertEquals(commits[1], commits[0].children.all()[0].child)
        self.assertEquals(commits[0], commits[1].parents.all()[0].parent)

