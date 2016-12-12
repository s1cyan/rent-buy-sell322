from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import Order, ShoppingCart, UserProfile
from ..date_checker import update_all


@login_required
def checkout(request):
    from ..date_checker import update_all

    """View for checkout page

    Buttons to handle: CONFIRM CHECKOUT, CANCEL
    """
    profile = UserProfile.objects.get(user=request.user)
    # cart_pk = request.POST.get("cart", "")
    context_dict = {
        'username': request.user.username,
        'money': profile.balance,
        # 'cart_pk': cart_pk,
    }
    # if "confirm_checkout" in request.POST:
    #     cart = ShoppingCart.objects.get(user=profile)
    #     order = Order.objects.create(
    #         user=profile,
    #         products=cart.products
    #     )
    #     order.save()
    #     return render(request, 'orders.html', context_dict)
    return render(request, 'checkout.html', context_dict)
