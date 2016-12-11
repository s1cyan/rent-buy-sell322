from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import User
from django.shortcuts import render
from ..models import Order, ShoppingCart, UserProfile, Rating
from decimal import Decimal


@login_required
def orders(request):
    # Render the page for previous orders
    profile = UserProfile.objects.get(user=request.user)
    context_dict = {
        'username': request.user.username,
        'money': profile.balance,
    }
    if "confirm_checkout" in request.POST:
        # TODO execute transactions, deduct from profile.balance
        # TODO deduct from quantities, and check to set product as inactive
        cart = ShoppingCart.objects.get(user=profile)
        new_order = Order(user=profile)
        new_order.save()
        new_order.products.add(*cart.products.all())
        for product in cart.products.all():
            print("PRODUCT TO DELETE:", product)
            product.is_active = False
            product.save()
            print(product.is_active)
        cart_total = cart.products.all().aggregate(Sum('price'))
        amount = cart_total['price__sum']
        print(amount)
        profile.balance -= amount
        profile.save()
        print(profile.balance)
        new_order.save()
        cart.delete()
    all_orders = Order.objects.filter(user=profile)
    # Check if previous orders exist
    if all_orders.count():
        orders_list = list(all_orders.all())
        order_dic = {}
        for order in orders_list:
            product_list = list(order.products.all())
            order_dic[str(order.pk)] = product_list
        context_dict['allorders'] = order_dic

    if "rating" in request.POST:
        rating_input = request.POST['rating']
        listed_seller = request.POST.get('seller', ' ')
        user_seller = User.objects.get(username = listed_seller)
        seller_profile = UserProfile.objects.get(user = user_seller)
        new_rating = Rating(user=seller_profile,rating = int(rating_input))
        new_rating.save()
        update_rating(seller_profile)
        print ("*******", rating_input, '****', listed_seller)
    return render(request, 'orders.html', context_dict)


def update_rating(seller_profile):
    rs = Rating.objects.filter(user = seller_profile)
    ratings = list(rs.values_list('rating', flat = True))
    overall_rating = float(float(sum(ratings))/float(len(ratings)))
    seller_profile.rbs_rating = Decimal(overall_rating)
    seller_profile.save()