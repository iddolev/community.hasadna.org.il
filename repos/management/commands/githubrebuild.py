from django.core.management.base import NoArgsCommand
from repos.models import Repo, Commit, CommitRepo
from repos.github_crawler import GithubCrawler
from pygithub3 import Github

class Command(NoArgsCommand):
    help = 'Closes the specified poll for voting'

    def handle_noargs(self, **options):

        self.stdout.write("Connecting to Github...")
        github = Github(login='', password='')
        ghc = GithubCrawler(github)

        self.stdout.write("Clearing commits from DB...")
        CommitRepo.objects.all().delete()
        Commit.objects.all().delete()

        self.stdout.write("Getting commits from Github and rebuilding DB...")
        #run the script to import all commits and rebuild db
        ghc.process_all_repos()

        self.stdout.write("Rebuild completed successfully!")
