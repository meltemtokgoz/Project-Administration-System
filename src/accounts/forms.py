from django import forms
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth.models import User
####################################################################

####################################################################
class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, label='User Name')
    password = forms.CharField(max_length=10, label='Password', widget=forms.PasswordInput)
    usertype = forms.CharField(max_length=10, label='User Type')

    @transaction.atomic
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        usertype = self.cleaned_data.get('usertype')
        if username and password:
            user = authenticate(username=username, password=password, usertype=usertype)
            if not user:
                raise forms.ValidationError('Username or password is not correct')
            return super(LoginForm, self).clean()

#####################################################################

#####################################################################
class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=30, label='Username')
    password1 = forms.CharField(max_length=30, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=30, label='Password Again', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]
    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_date.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords are not the same")
        return password2
#####################################################################
