# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from .forms import UserForm, SellForm, SearchForm, ComplaintForm
# Create your views here.

def register(request):
    '''signup page view'''
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'],
                email=user_form.cleaned_data['email']
                )
            user.save()

            registered = True

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors)
    else:
        # Not a HTTP POST, so we render our form using the ModelForm instance.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        # profile_form = UserProfileForm()
    # Render the template depending on the context.
    return render(request, 'registration.html',
                  {'user_form': user_form,
                   'registered': registered})



def redir(request):
    '''TODO redirection for top nav bar'''
    return redirect('/rbs')

def add_withdraw(request):
    return render(request, 'add_withdraw.html')

def cart(request):
    return render(request, 'cart.html')


def confirm_checkout(request):
    return render(request, 'confirm_checkout.html')


def edit_listings(request):
    return render(request, 'edit_listings.html')


def file_complaint(request):
    complaint_form = ComplaintForm(request.POST)
    context_dict = {
        'complaint-form': complaint_form,
        'process_complaint': '/rbs/submitted-complaint'
    }
    return render(request, 'file_complaint.html', context_dict)


def process_complaint(request):
    '''
    *** Put the functions to process complaints and send them to db here - same method as the others
    do request.POST['name value in template'] to access values 
    :param request:
    :return:
    '''
    print (request.POST)
    return render(request,'complaint_submitted.html')


def sell_item(request):
    '''
    :param request:
    :return:
    has the sell form, sends the return values to process the request at function process_sell()
    '''

    sell_form = SellForm(request.POST)
    context_dict = {
        'sell_form': sell_form,
        'process_sell_post': '/rbs/process-listing'
    }
    return render(request, 'sell_item.html',context_dict)


def process_sell(request):
    """
    have the functions for search processing in here
    to access the values in the SellForm, do request.POST['name value in template']
    """
    print (request.POST) # just for checking the values returned in terminal
    return render(request, 'sell_processed.html')


def show_results(request):
    search_form = SearchForm(request.GET)

    '''
    write ur model lookup stuff here and return the stuff you find. Check the results template for the values you need to return per item
    '''

    return render(request, 'results.html')


def update_account(request):
    return render(request, 'update_info.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('user'))
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


