from repos.models import Project, Repo, ProjectOwner
from users.models import User
import floppyforms as forms


class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project


class AddRepoToProject(forms.ModelForm):
    class Meta:
        model = Repo
        fields = ['full_name']


class AddOwnerToProject(forms.Form):
    owner = forms.ModelChoiceField(queryset=User.objects.all())
