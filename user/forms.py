from django.contrib.auth.forms import UserCreationForm
# from django.forms import forms
from django import forms
# from catalog.forms import StyleFormMixin
from user.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Введите ваш адрес электронной почты")
    new_password = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)

