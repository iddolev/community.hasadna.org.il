from users.models import User
from django import forms


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password','nick','privacy','email_privacy','english_name','hebrew_name','biography','github_username']



