from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from ..forms import UserForm, UserForm_Django
from ..models import UserProfile
from ..date_checker import update_all



@login_required
def update_account(request):
    """
    Update the user profile
    """
    update_all()

    user = User.objects.get(user=request.user.id)
    profile = UserProfile.objects.get(user=request.user)

    user_form = UserForm_Django(instance=user)
    ProfileInlineFormset = inlineformset_factory(User,
                                                 UserProfile,
                                                 fields=('bio',
                                                         'phone',
                                                         'city',
                                                         'country',
                                                         'transactions',
                                                         'credit_card',
                                                         'strikes',
                                                         'suspensions',
                                                         'rbs_vip_user'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm_Django(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES or None, instance=user)
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES or None, instance=created_user)
                if formset.is_valid():
                    user = User.objects.get(user=request.user.id)
                    profile = UserProfile.objects.get(user=request.user)
                    if profile.balance >= 5000.00 and profile.transactions >= 5 and profile.suspensions == 0 and profile.strikes == 0:
                        profile.rbs_vip_user = True
                        print(profile.rbs_vip_user)
                        print(profile.suspensions)
                        print("i made it ---- true")
                    else:
                        profile.rbs_vip_user = False
                        print("i made it --- false")
                        print(profile.rbs_vip_user)
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/rbs/update')

        return render(request, "update-info.html", {
            'username': request.user.username,
            'money': profile.balance,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
