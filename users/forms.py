from users.models import User
import floppyforms as forms

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['privacy','password','nick',
                  'english_name','hebrew_name','email','email_privacy',
                  'phone_number','phone_privacy',
                  'facebook_username','facebook_privacy',
                  'biography','github_username']