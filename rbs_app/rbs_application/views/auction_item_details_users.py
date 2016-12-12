from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..associate import associate_option
from ..models import Product, UserProfile
from ..date_checker import update_all


@login_required
def auction_item_details_users(request):
    # update_all()
    profile = UserProfile.objects.get(user=request.user)

    context_dict = {
        'user': request.user.username,
        'money': profile.balance,
        'user.is_authenticated': True,

    }
    if request.method == 'POST':
        bid = request.POST.get('bidamount','')
        bid = Decimal(bid)
        product_pk = request.POST.get('pk', '')
        product = Product.objects.get(pk=product_pk)
        context_dict = {
            'user': request.user.username,
            'money': profile.balance,
            'user.is_authenticated': True,

        }
        if bid > product.price and profile.balance >= bid:
            if product.current_bidder is not None:  # get last users profile if the item has been prevously bid on
                last_bidder = UserProfile.objects.get(pk=product.current_bidder)
                print ("##########", last_bidder)
                last_bidder.balance += product.price  # take their balance += product's current price
                last_bidder.save()

            product.price = bid  # update the current price
            product.current_bidder = profile.pk # update the current bidder
            profile.balance -= bid # subtract from that user's balance

            profile.save()
            product.save()
        # print ("********** user is authenticated", request.user.is_authenticated)
        context_dict['money'] = profile.balance
        # context_dict['item'] = product.title
        # context_dict['price'] = product.price
        # context_dict['seller'] = product.seller
        context_dict['option'] = associate_option(product.option)
        # context_dict['description'] = product.description
        context_dict['product_pk'] = product_pk
        context_dict['product_id'] = product.id
        context_dict['product'] = product
        context_dict['time'] = product.takedown_time
        HttpResponseRedirect('item-auction')
        # return render(request, 'user_auction_details', context_dict)

    return render(request,'auction_details.html', context_dict)