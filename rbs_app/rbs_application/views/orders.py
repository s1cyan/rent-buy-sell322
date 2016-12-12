from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from ..models import Order, ShoppingCart, UserProfile


@login_required
def orders(request):
    # Render the page for previous orders
    profile = UserProfile.objects.get(user=request.user)
    context_dict = dict()
    if "confirm_checkout" in request.POST:
        # TODO execute transactions, deduct from profile.balance
        # TODO deduct from quantities, and check to set product as inactive
        cart = ShoppingCart.objects.get(user=profile)
        new_order = Order(user=profile)
        new_order.save()
        new_order.products.add(*cart.products.all())
        for product in cart.products.all():
            seller = UserProfile.objects.get(user=product.seller)
            print("\n\nTransaction for", product, "sold by", seller)
            print("Seller balance BEFORE:", seller.balance)
            print("Buyer balance BEFORE:", cart.user.balance)
            seller.balance += product.price
            seller.save()
            cart.user.balance -= product.price
            cart.user.save()
            print("TRANSACTION DONE!!!!!!!!!!!!!!!!!")
            print("Seller balance AFTER:", seller.balance)
            print("Buyer balance BEFORE:", cart.user.balance)
            product.is_active = False
            product.save()
            print(product.is_active)
        cart_total = cart.products.all().aggregate(Sum('price'))
        amount = cart_total['price__sum']
        print("CART TOTAL was: $", amount)
        # profile.balance -= amount
        # profile.save()
        # print(profile.balance)
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
    context_dict['username'] = request.user.username
    # context_dict['money'] = profile.balance
    return render(request, 'orders.html', context_dict)
