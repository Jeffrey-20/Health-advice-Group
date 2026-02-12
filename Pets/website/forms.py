
import django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms.widgets import PasswordInput, TextInput

# The SignUpForm class inherits from UserCreationForm and specifies the fields that will be included in the form: username, email, password1, and password2. This form will be used for user registration, allowing new users to create an account by providing their username, email, and password.
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# The LoginForm class inherits from AuthenticationForm and defines two fields: username and password. The username field uses a TextInput widget, while the password field uses a PasswordInput widget to ensure that the password is not displayed in plain text when entered.
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

