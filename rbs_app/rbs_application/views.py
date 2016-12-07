# Create your views here.
import decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from .forms import AddWithdrawForm, UserForm, SellForm, SearchForm, ComplaintForm, RegistrationForm
from .models import UserProfile, Product, Category, Complaint, ShoppingCart
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
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
    profile = UserProfile.objects.get(user=request.user)
    add_withdraw_form = AddWithdrawForm(request.POST)
    if request.method == 'POST':
        if request.POST['add']:
            add = decimal.Decimal(request.POST['add'])
            profile.balance += add
            profile.save()
        if request.POST['withdraw']:
            withdraw = decimal.Decimal(request.POST['withdraw'])
            profile.balance -= withdraw
            profile.save()
        return HttpResponseRedirect(reverse('user'))
    else:
        return render(request, 'add_withdraw.html',
                      {'add_withdraw_form': add_withdraw_form,
                       'username': request.user.username,
                       'money': profile.balance})


@login_required
def edit_listings(request):
    profile = UserProfile.objects.get(user=request.user)
    context_dict = {
        'user': request.user.username,
        'money': profile.balance,
    }
    return render(request, 'edit_listings.html', context_dict)


def file_complaint(request):
    complaint_form = ComplaintForm(request.POST)
    profile= UserProfile.objects.get(user=request.user)
    context_dict = {
        'username': request.user.username,
        'money':profile.balance,
        'complaint-form': complaint_form,
        'process_complaint': '/rbs/submitted-complaint',
    }

    return render(request, 'file_complaint.html', context_dict)


def process_complaint(request):
    '''
    *** Put the functions to process complaints and send them to db here - same method as the others
    do request.POST['name value in template'] to access values
    Users can submit a complaint for a user, if they get the username wrong
    users will be told they submitted a complaint, but it will not necessarily be registered
    bc the user has to be in our system
    :param request:
    :return:
    '''
    profile= UserProfile.objects.get(user=request.user)
    context_dict = {
        'username': request.user.username,
        'money': profile.balance,

    }
    if User.objects.filter(username=request.POST['reported_user']).exists():
        complained_user = User.objects.get(username = request.POST['reported_user'])
        complaint_user_profile = UserProfile.objects.get(user = complained_user)
        complaint_str = request.POST['complaint']
        complaint = Complaint( user_id = complaint_user_profile,
                               complaint = complaint_str)
        complaint.save()
    return render(request,'complaint_submitted.html', context_dict)

@login_required
def sell_item(request):
    '''
    :param request:
    :return:
    has the sell form, sends the return values to process the request at function process_sell()
    '''

    sell_form = SellForm(request.POST)
    profile = UserProfile.objects.get(user=request.user)
    context_dict = {
        'username': request.user.username,
        'money': profile.balance,
        'sell_form': sell_form,
        'process_sell_post': '/rbs/process-listing'
    }
    return render(request, 'sell_item.html', context_dict)

@login_required
def process_sell(request):
    profile = UserProfile.objects.get(user=request.user)

    context_dict = {
        'user': request.user.username,
        'money': profile.balance,
    }
    """
    have the functions for search processing in here
    to access the values in the SellForm, do request.POST['name value in template']
    """
    print (request.POST) # just for checking the values returned in terminal
    # if fields are blank redirect back to refill the form
    if (request.POST['item'] or request.POST['price'] or request.POST['daymonth']or request.POST['time'] or request.POST['description']) == None:
        print("invalid entry ")
        return HttpResponseRedirect('sell')

    # create the Product entry

    product = Product(seller=request.user,
                      title = request.POST['item'],
                      text = request.POST['description'],
                      takedown_date = request.POST['daymonth'],
                      takedown_time = request.POST['time'],
                      quantity = request.POST['quantity'],
                      price = request.POST['price'],

                      # TODO Change status to a boolean field, Charfield will make it harder to tell what is an active listing
                      # Maybe even change its name to is_active_listing
                      # Also maybe get rid of categories?
                      )
    product.save()
    return render(request, 'sell_processed.html', context_dict)


def show_results(request):
    # Searching for products is handled by this function
    context_dict = dict()
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        context_dict['username'] = request.user.username
        context_dict['money'] = profile.balance
    (query, method, min, max) = (request.GET['query'],
                                 request.GET['method'],
                                 request.GET['minprice'],
                                 request.GET['maxprice'], )
    results = Product.objects.filter(option=method)
    print("ALL RESULTS: ", results)
    if query: # TODO add logic to check for whitespace
        results = Product.objects.filter(title__icontains=query, option=method)
        (context_dict['results'], context_dict['found']) = (results, True)
        if not results:
            (context_dict['results'], context_dict['found']) = (results, False)
    else:
        (context_dict['results'], context_dict['found']) = (results, True)
    return render(request, 'results.html', context_dict)


def details(request):
    # View for clicking 'View item details' in search results
    context_dict = dict()
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        context_dict['username'] = request.user.username
        context_dict['money'] = profile.balance
    product_pk = request.POST.get('pk', '')
    product = Product.objects.get(pk=product_pk)
    context_dict['item'] = product.title
    context_dict['price'] = product.price
    context_dict['seller'] = product.seller.username
    context_dict['option'] = product.option
    context_dict['description'] = product.text
    context_dict['product_pk'] = product_pk
    # context_dict['product_id'] = product.id
    return render(request, 'user_item_details.html', context_dict)
    # TODO JONATHAN, delete this later. NOBODY TOUCH THESE COMMENTED OUT LINES
    # because multiple item can have the same name, access by pk
    # if request.method == "POST":
        # if request.user.is_authenticated: # need to check if its not auction, and if item is an auction item, redirect to an auction page
            # GOing to the item details page
            # if the item is clicked on, load the item details page with the Product information
            # profile = UserProfile.objects.get(user=request.user)
            # product_pk = request.POST.get('pk', '')
            # product = Product.objects.get(pk=product_pk) # bc multiple item can have the same name, access by pk
            # context_dict = {
            #     'user': request.user.username,
            #     'money': profile.balance,
            #     'item': product.title,
            #     'price': product.price,
            #     'seller': product.seller.username,
            #     'option': 'n/a yet', # TODO SET THE SELLING TYPE
            #     'description': product.text,
            #     'product_pk': product.pk
            # }
            # return HttpResponse("HERE")
            # return render(request,'user_item_details.html',context_dict)
        # else:
        #     product_pk = request.POST.get('pk', '')
        #     product = Product.objects.get(pk=product_pk)  # bc multiple item can have the same name, access by pk
        #     context_dict = {
        #         'item': product.title,
        #         'price': product.price,
        #         'seller': product.seller.username,
        #         'option': 'n/a yet',  # TODO SET THE SELLING TYPE
        #         'description': product.text,
        #         'product_pk': product.pk
        #     }
        #     return render(request,'visitor_item_details.html',context_dict)

    # return render(request, template, context_dict)
    # needs catch statement if product.objects.get != search form...

    # return render(request, template, context)
    pass


@login_required
def buy_item_details_users(request):
    profile = UserProfile.objects.get(user=request.user)

    context_dict = {
        'user': request.user.username,
        'money': profile.balance,
        'user.is_authenticated': True,

    }
    if request.method == "POST":
        product_pk = request.POST.get('pk','')
        product = Product.objects.get(pk = product_pk) # access the product, do what you will with it
        # TODO Add to shopping cart logic
    return render(request,'user_item_details.html', context_dict)

@login_required
def auction_item_details_users(request):
    if request.method == 'POST':
        product_pk = request.POST.get('pk','')
        product_for_auction = Product.objects.get(pk= product_pk) # access to the product for auction, do w.e you need
    return render(request,'user_auction_details.html')

def item_details_visitor(request):
    return render(request,'visitor_item_details.html')


@login_required
def cart(request):
    profile = UserProfile.objects.get(user=request.user)
    context_dict = {
        'username': request.user.username,
        'money': profile.balance,
        # 'cart' : cart,
    }
    # check if "Add Item to Cart" was pressed
    if request.method == 'POST':
        # Show which product was added to cart
        product_pk = request.POST.get('pk')
        product = Product.objects.get(pk=product_pk)
        product.save()
        cart = ShoppingCart.objects.get_or_create(user=profile)[0]
        cart.save()
        cart.products.add(product)
        cart.save()
        context_dict['products'] = cart.products.all()
        return render(request, 'cart.html', context_dict)
    else:
        cart = ShoppingCart.objects.get_or_create(user=profile)[0]
        print(cart.products.all())
        context_dict['products'] = cart.products.all()
        return render(request, 'cart.html', context_dict)

@login_required
def confirm_checkout(request):
    return render(request, 'confirm_checkout.html')

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

        return render(request, "update_info.html", {
            'username': request.user.username,
            'money': profile.balance,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied


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
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the blank dictionary object...
        return render(request, 'login.html', {})

@login_required
def user_main(request):
    profile = UserProfile.objects.get(user=request.user)
    context_dict={
        'username': request.user.username,
        'money': profile.balance,
    }
    print ( "####### ", profile.balance)
    if request.user.is_authenticated:
        if profile.verified_by_admin == True:
            print(profile.verified_by_admin)
            return render(request, 'user_main.html', context_dict)
        else:
            return HttpResponse("You have not been verified by an admin")

@login_required
def view_previous_orders(request):
    # Render the page for previous orders
    profile = UserProfile.objects.get(user=request.user)
    context_dict = {
        'username': request.user.username,
        'money': profile.balance,
    }
    return render(request, 'previous_orders.html', context_dict)


def visitors_main(request):
    # Redirect to visitor home page
    return render(request, 'visitors_main.html')


# @login_required
def user_logout(request):
    logout(request)
    # Redirect to visitor home page
    return HttpResponseRedirect(reverse('visitor'))
