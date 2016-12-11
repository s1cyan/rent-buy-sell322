from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from ..forms import UserForm
from ..models import UserProfile


@login_required
def update_account(request):
    """
    Update the user profile
    """

    user = User.objects.get(user=request.user.id)
    profile = UserProfile.objects.get(user=request.user)

    user_form = UserForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User,
                                                 UserProfile,
                                                 fields=('bio',
                                                         'phone',
                                                         'city',
                                                         'country',
                                                         'transactions',
                                                         'credit_card',
                                                         'strikes',
                                                         'suspensions',))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES or None, instance=user)
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES or None, instance=created_user)
                if formset.is_valid():
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