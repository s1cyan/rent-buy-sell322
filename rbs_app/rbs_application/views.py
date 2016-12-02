# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from .forms import UserForm, SellForm, SearchForm, ComplaintForm, RegistrationForm
from .models import UserProfile, Product
# Create your views here.

def register(request):
    '''signup page view'''
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        # registration_form = RegistrationForm(data=request.POST)
        if user_form.is_valid(): # and registration_form.is_valid():
            user = User.objects.create_user(
                first_name=user_form.cleaned_data['first_name'],
                last_name=user_form.cleaned_data['last_name'],
                username=user_form.cleaned_data['username'],
                email=user_form.cleaned_data['email'],
                password=user_form.cleaned_data['password'],
                # password2=user_form.cleaned_data['password2'],
                )
            user.save()

            # userprofile = UserProfile.objects.get_or_create(
            #     first_name=registration_form.cleaned_data['first_name'],
            #     last_name=registration_form.cleaned_data['last_name'],
            #     city=registration_form.cleaned_data['city'],
            #     country=registration_form.cleaned_data['country']
            # )
            # userprofile.save()

            registered = True

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors)
    else:
        # Not a HTTP POST, so we render our form using the ModelForm instance.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        # registration_form = RegistrationForm()
        # profile_form = UserProfileForm()
    # Render the template depending on the context.
    return render(request, 'registration.html',
                  {'user_form': user_form,
                   # 'registration_form': registration_form,
                   'registered': registered})


def redir(request):
    '''TODO redirection for top nav bar'''
    return redirect('/rbs')

@login_required
def add_withdraw(request):
    return render(request, 'add_withdraw.html')

@login_required
def cart(request):
    return render(request, 'cart.html')

@login_required
def confirm_checkout(request):
    return render(request, 'confirm_checkout.html')

@login_required
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

@login_required
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

@login_required
def process_sell(request):
    """
    have the functions for search processing in here
    to access the values in the SellForm, do request.POST['name value in template']
    """
    print (request.POST) # just for checking the values returned in terminal
    return render(request, 'sell_processed.html')

def show_results(request):
    search_form = request.GET['search_input']

    if 'rent_option' in request:
        rent_option = request.GET['rent_option']
    else:
        rent_option = 'off'
    if 'buy_option' in request:
        buy_option = request.GET['buy_option']
    else:
        buy_option = 'off'
    if 'auction_option' in request:
        auction_option = request.GET['auction_option/']
    else:
        auction_option = 'off'
    min_price = request.GET['minprice']
    if min_price == '':
        min_price = 0
    max_price = request.GET['maxprice/']
    if max_price == '':
        max_price = 99999.99

    print(search_form, rent_option, buy_option, auction_option, min_price, max_price)

    if search_form == '':
        products = Product.objects.all()
        context = {'products': products}
        template = 'results.html'
        print(context)
        return render(request, template, context)
    products = Product.objects.all()
    context = {'products': products}
    template = 'results.html'
    if Product.objects.get(title=search_form):
        products = Product.objects.all()
        searched_context = Product.objects.get(title=search_form)
        return render(request, 'user_item_details.html')

    '''
    write ur model lookup stuff here and return the stuff you find. Check the results template for the values you need to return per item
    '''
    return render(request, template, context)

@login_required
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

@login_required
def user_main(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.user.is_authenticated:
        if profile.verified_by_admin == True:
            print(profile.verified_by_admin)
            return render(request, 'user_main.html')
        else:
            return HttpResponse("You have not been verified by an admin")

@login_required
def view_previous_orders(request):
    return render(request, 'previous_orders.html')


def visitors_main(request):
    return render(request, 'visitors_main.html')


# @login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('visitor'))
