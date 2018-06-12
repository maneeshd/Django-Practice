from django.forms import Form, CharField, PasswordInput, ModelForm, ValidationError
from django.contrib.auth.models import User


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput(attrs={'autocomplete': 'off'}))


class UserRegistrationForm(ModelForm):
    password = CharField(label='Password',
                         widget=PasswordInput(attrs={'autocomplete': 'off'}))
    password2 = CharField(label='Repeat password',
                          widget=PasswordInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')


    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['password2']:
            raise ValidationError("Passwords don't match.")
        return cleaned_data['password2']
