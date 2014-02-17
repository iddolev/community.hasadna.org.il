from repos.models import Project, Repo
import floppyforms as forms


class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project


class AddRepoToProject(forms.ModelForm):
    class Meta:
        model = Repo
        fields = ['full_name']