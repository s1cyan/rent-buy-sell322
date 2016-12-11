from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ..models import UserProfile

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                profile = UserProfile.objects.get(user=user)
                if profile.verified_by_admin == True:
                    login(request, user)
                    context_dict = {
                        'username': request.user.username,
                        'money': profile.balance,
                    }
                    # Redirect to a success page.
                    # return HttpResponseRedirect(reverse('index'))
                    return render(request, 'index.html', context_dict)
                else:
                    return HttpResponse("You've not been verified by an admin.")
            else:
                # Return a 'disabled account' error message
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the blank dictionary object...
        return render(request, 'login.html', {})