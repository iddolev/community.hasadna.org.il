from pygithub3 import Github, services



gh = Github(login='omridor', password='Gnrhsur42')

omri = gh.users.get() # Auth required

choi = gh.repos.get(user='omridor', repo='community.hasadna.org.il')


commits_service=services.repos.Commits(login='omridor', password='Gnrhsur42')

choi_commits = commits_service.list(user='omridor',repo='community.hasadna.org.il')
print choi_commits.all()

commit = choi_commits.all()[0]