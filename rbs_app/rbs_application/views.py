# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from .forms import *
# Create your views here.

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

# @csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username_id'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, { 'form': form })

    return render_to_response('registration.html',variables,)


def process_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user( username=form.cleaned_data['username_id'], password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'] )
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, { 'form': form })

    return render_to_response('registration.html',variables,)


def view_previous_orders(request):
    return render(request, 'previous_orders.html')


def visitors_main(request):
    return render(request, 'visitors_main.html')




# @login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('visitor'))



# @login_required
# def home(request):
#     return render_to_response(
#     'home.html',
#     { 'user': request.user }
#     )


# def register_success(request):
#     return render_to_response(
#     'registration/success.html',
#     )
