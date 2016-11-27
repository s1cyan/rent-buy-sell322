''' Forms for registration page.
    Information grabbed: username, email, password

    Thanks to original developer: Connie Liu '''

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

''' CONNIE'S CODE
class RegistrationForm(forms.Form):

    password2 = forms.CharField(
    widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
    label=_("Password (again)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Passwords did not match! Please Try Again."))
        return self.cleaned_data
'''
class UserForm(forms.Form):
    ''' User registration form for RBS '''
    username = forms.RegexField(
        regex=r'^\w+$', widget=forms.TextInput(
        attrs=dict(required=True, max_length=30)), label=_("USERNAME *"), error_messages={ 'invalid':_("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("EMAIL ADDRESS *"))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("PASSWORD *"))

    def clean_username(self):
        ''' Clean form data for username '''
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        ''' Clean form data for password '''
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Passwords did not match! Please Try Again."))
        return self.cleaned_data
