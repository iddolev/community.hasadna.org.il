from users.models import User
import floppyforms as forms

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password','nick','privacy','email_privacy',
                  'english_name','hebrew_name','biography','github_username']