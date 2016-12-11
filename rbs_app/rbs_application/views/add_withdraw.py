from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..models import UserProfile
from ..forms import AddWithdrawForm

@login_required
def add_withdraw(request):
    """Add/Withdraw Money Page View

    A User is able to add or withdraw money from this page.

    Returns:
    """
    profile = UserProfile.objects.get(user=request.user)
    add_withdraw_form = AddWithdrawForm(request.POST)
    if request.method == 'POST':
        if request.POST['add']:
            add = Decimal(request.POST['add'])
            profile.balance += add
            profile.save()
        if request.POST['withdraw']:
            withdraw = Decimal(request.POST['withdraw'])
            profile.balance -= withdraw
            profile.save()
        return HttpResponseRedirect(reverse('user'))
    else:
        return render(request, 'add-withdraw.html',
                      {'add_withdraw_form': add_withdraw_form,
                       'username': request.user.username,
                       'money': profile.balance})