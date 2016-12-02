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
            attrs=dict(required=True, max_length=30)), label=_("USERNAME *"),
        error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
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


class SellForm(forms.Form):
    SELL_CHOICES = ((1, 'RENT'), (2, 'BUY NOW'), (3, 'AUCTION'))

    item_name = forms.CharField(max_length=64)
    sell_choice = forms.ChoiceField(choices=SELL_CHOICES)
    price = forms.DecimalField()
    takedown_date = forms.SelectDateWidget()
    takedown_time = forms.TimeField()
    description = forms.CharField(max_length=128)


class SearchForm(forms.Form):
    item_name = forms.CharField(max_length=128)
    search_rent = forms.BooleanField()
    search_buy = forms.BooleanField()
    search_auction = forms.BooleanField()
    min_price = forms.IntegerField()
    max_price = forms.IntegerField()

class ComplaintForm(forms.Form):
    reported_user = forms.CharField(max_length=64)
    complaint = forms.CharField(max_length=128)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    username = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.CharField(max_length=64)
    confirm_password = forms.CharField(max_length=64)
    address = forms.CharField()
    credit_card = forms.IntegerField(max_value=9999999999999999)
    math_answer = forms.IntegerField()
