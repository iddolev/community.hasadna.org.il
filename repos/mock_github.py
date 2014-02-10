from datetime import datetime


class Object(object):
    pass


class MockGithub():
    def __init__(self):
        self.repos = Object()
        self.repos.commits = MockCommitsService()

    def add_mock_commit(self, user, repo, commit):
        return self.repos.commits.add_mock_commit(user, repo, commit)


class MockCommitsService:
    def __init__(self):
        self.fullname_to_commits = dict()
        pass

    def add_mock_commit(self, user, repo, commit):
        fullname = '/'.join([user, repo])
        if fullname not in self.fullname_to_commits.keys():
            self.fullname_to_commits[fullname] = []
        self.fullname_to_commits[fullname].append(commit)

    def list(self, user, repo):
        fullname = '/'.join([user, repo])
        if fullname not in self.fullname_to_commits.keys():
            return []
        return MockResult(self.fullname_to_commits[fullname])

class MockResult(list):
    def all(self):
        return self


class MockCommit:
    def __init__(self,
                 sha,
                 parent_shas=[],
                 author_username='foo',
                 author_name='Foo',
                 author_url='x',
                 author_email='x',
                 committer_username='foo',
                 committer_name='Foo',
                 committer_url='x',
                 committer_email='x',
                 url='x',
                 message='x',
                 author_date=datetime.utcnow(),
                 committer_date=datetime.utcnow(),
                 ):
        author = Object()
        author.login = author_username
        author.name = author_name
        author.url = author_url
        author.email = author_email
        author.date = author_date

        committer = Object()
        committer.login = committer_username
        committer.name = committer_name
        committer.url = committer_url
        committer.email = committer_email
        committer.date = committer_date

        self.author = author
        self.committer = committer
        self.commit = Object()
        self.commit.author = author
        self.commit.committer = committer
        self.commit.message = message

        self.sha = sha
        self.url = url
        self.parents = []
        for parent_sha in parent_shas:
            parent = Object()
            parent.sha = parent_sha
            self.parents.append(parent)