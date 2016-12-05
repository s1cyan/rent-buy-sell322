""" Forms for RBS"""

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta

class UserForm(forms.Form):
    """ User registration form for RBS """
    first_name = forms.CharField(label=_("FIRST NAME *"), max_length=10)
    last_name = forms.CharField(label=_("LAST NAME *"), max_length=10)
    username = forms.RegexField(
        label=_("USERNAME *"),
        regex=r'^\w+$',
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(
        label=_("EMAIL ADDRESS *"),
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)))
    password = forms.CharField(
        label=_('PASSWORD *'),
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)))
    password2 = forms.CharField(
        label=_("CONFIRM PASSWORD *"),
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)))

    def clean_username(self):
        """ Clean form data for username """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        """ Clean form data for password """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Passwords did not match! Please Try Again."))
        return self.cleaned_data


class SellForm(forms.Form):
    SELL_CHOICES = ((1, 'RENT'), (2, 'BUY NOW'), (3, 'AUCTION'))

    item_name = forms.CharField(max_length=64)
    sell_choice = forms.ChoiceField(choices=SELL_CHOICES)
    price = forms.DecimalField()
    takedown_date = forms.DateField(widget=forms.SelectDateWidget(),
                                    initial=datetime.today().date() + timedelta(days=7))
    takedown_time = forms.TimeField(initial=datetime.now().time())
    description = forms.CharField(max_length=128)


class SearchForm(forms.Form):
    item_name = forms.CharField(max_length=128)
    search_rent = forms.BooleanField()
    search_buy = forms.BooleanField()
    search_auction = forms.BooleanField()
    min_price = forms.IntegerField()
    max_price = forms.IntegerField()


class AddWithdrawForm(forms.Form):
    add = forms.DecimalField(label="Add Money", initial=1000)
    withdraw = forms.DecimalField(label="Withdraw Money", initial=22)


class ComplaintForm(forms.Form):
    reported_user = forms.CharField(max_length=64)
    complaint = forms.CharField(max_length=128)


class RegistrationForm(forms.Form):
    city = forms.CharField()
    country = forms.CharField()
    credit_card = forms.CharField(max_length=16)
    math_answer = forms.IntegerField()

class UserForm(forms.ModelForm):
    """
    The default form for a user
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
