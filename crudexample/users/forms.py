from django import forms
from .models import Users

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['firstName', 'lastName', 'emailId', 'password']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
