from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import UserProfile, Product
from ..date_checker import update_all

@login_required
def buy_item_details_users(request):
    update_all()
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
    return render(request, 'item-details.html', context_dict)