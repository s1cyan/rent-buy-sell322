from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..models import Product, UserProfile

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
    # print (request.POST) # just for checking the values returned in terminal
    # if fields are blank redirect back to refill the form
    if (request.POST['item'] or request.POST['price'] or request.POST['daymonth']or request.POST['time'] or request.POST['description']) == None:
        # print("invalid entry ")
        return HttpResponseRedirect('sell')

    # create the Product entry
    product = Product(seller=request.user,
                      title = request.POST['item'],
                      text = request.POST['description'],
                      takedown_date = request.POST['daymonth'],
                      takedown_time = request.POST['time'],
                      quantity = request.POST['quantity'],
                      price = request.POST['price'],
                      option=request.POST['sell_select'],
                      )
    product.save()
    # print(product)
    return render(request, 'sell_processed.html', context_dict)