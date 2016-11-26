# Create your views here.
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username_id'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, { 'form': form })

    return render_to_response('registration.html',variables,)


def view_previous_orders(request):
    return render(request, 'previous_orders.html')


def visitors_main(request):
    return render(request, 'visitors_main.html')





# def logout_page(request):
#     logout(request)
#     return HttpResponseRedirect('/')



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
