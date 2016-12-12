from django.contrib.auth.models import User
from django.shortcuts import render
from ..forms import UserForm
from ..date_checker import update_all
from random import randint

def register(request):
    """Registration Page View

    Displays registration form for user to fill up.
    If it's a POST request, uses the user input to make a new User.

    Returns: {% url 'register' %}
    """
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    update_all()
    x = randint(0,9)
    y = randint(0,9)
    math_equation = str(x) +'+' + str(y) + '='
    context_dict= {
        'math': math_equation
    }
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        eq = request.POST.get('eq','')
        form_ans = request.POST.get('answer')
        ans = int( eq[0]) + int (eq[2])

        if user_form.is_valid() and int(form_ans) == int(ans) : # and registration_form.is_valid():
            user = User.objects.create_user(
                first_name=user_form.cleaned_data['first_name'],
                last_name=user_form.cleaned_data['last_name'],
                username=user_form.cleaned_data['username'],
                email=user_form.cleaned_data['email'],
                password=user_form.cleaned_data['password'],
                )
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    # Render the template depending on the context.
    return render(request, 'registration.html',
                  {'user_form': user_form,
                   'registered': registered, 'math': math_equation})