# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from .forms import UserForm
# Create your views here.

def register(request):
    '''signup page view'''
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of only the UserForm
        user_form = UserForm(data=request.POST)
        # profile_form = UserProfileForm(data=request.POST)

        # If the two forms is valid...
        if user_form.is_valid():
            user = User.objects.create_user(
            username=user_form.cleaned_data['username'],
            password=user_form.cleaned_data['password'],
            email=user_form.cleaned_data['email']
            )
            user.save()

            # user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            # user.set_password(user.password)
            # user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            # profile = profile_form.save(commit=False)
            # profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            # if 'picture' in request.FILES:
                # profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            # profile.save()

             # Update our variable to indicate that the template
             # registration was successful.
            registered = True

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances. # These forms will be blank, ready for user input.
        user_form = UserForm()
        # profile_form = UserProfileForm()
    # Render the template depending on the context.
    return render(request, 'registration.html',
                      {'user_form': user_form,
                       'registered': registered})



def redir(request):
    '''redirection'''
    return redirect('/rbs')

def add_withdraw(request):
    return render(request, 'add_withdraw.html')

def cart(request):
    return render(request, 'cart.html')


def confirm_checkout(request):
    return render(request, 'confirm_checkout.html')


def file_complaint(request):
    return render(request, 'file_complaint.html')


# def login(request):
#     return render(request, 'login.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('user_main'))
            else:
                # Return a 'disabled account' error message
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
        # The request is not a HTTP POST, so display the login form. # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the # blank dictionary object...
        return render(request, 'login.html', {})

def user_main(request):
    return render(request, 'user_main.html')


def view_previous_orders(request):
    return render(request, 'previous_orders.html')


def visitors_main(request):
    return render(request, 'visitors_main.html')


# @login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('visitor'))
