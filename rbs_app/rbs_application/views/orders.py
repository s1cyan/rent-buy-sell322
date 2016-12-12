from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import User
from django.shortcuts import render
from ..models import Order, ShoppingCart, UserProfile, Rating, Complaint, Product
from ..check_vip import  check_vip
from ..update_rating import update_rating
from ..date_checker import update_all


@login_required
def orders(request):
    # Render the page for previous orders
    profile = UserProfile.objects.get(user=request.user)
    context_dict = dict()
    update_all()
    if "confirm_checkout" in request.POST:
        cart = ShoppingCart.objects.get(user=profile)
        #print("\n\n",cart.products.all,"\n\n")
        #totalPrice=0
        #for i in cart:
        #    totalPrice+=double(i.price)

        print("\n\n", float(cart.products.all().aggregate(Sum('price'))['price__sum']), profile.balance, "\n\n")
        if float(cart.products.all().aggregate(Sum('price'))['price__sum']) > profile.balance:
            context_dict['username'] = request.user.username
            context_dict['money'] = profile.balance
            context_dict['messages']="You do not have enough money on your account for these purchases."
            return render(request, 'badAction.html', context_dict)

        new_order = Order(user=profile)
        new_order.save()
        new_order.products.add(*cart.products.all())
        for product in cart.products.all():
            seller = product.seller
            seller.balance += product.price
            seller.save()
            profile.balance -= product.price
            profile.save()
            product.quantity -= 1
            if product.quantity == 0:
                product.is_active = False
                product.save()
        profile.transactions += len(cart.products.all())
        profile.save()
        # cart_total = cart.products.all().aggregate(Sum('price'))
        # print("++++++++++++++++++ CART TOTAL IS:", cart_total)
        # amount = cart_total['price__sum']
        new_order.totalPrice = cart.totalPrice
        print("++++++++ NEW ORDER TOTALING:", new_order.totalPrice)
        # print("CART TOTAL was: $", amount)
        #context_dict['totalPrice'] = new_order.totalPrice
        new_order.save()
        cart.delete()
    all_orders = Order.objects.filter(user=profile)
    #print(all_orders[0].totalPrice)
    # Check if previous orders exist
    if all_orders.count():
        orders_list = list(all_orders.all())
        order_dic = dict()

        for order in orders_list:
            product_dic = dict()
            # print("*************", order.totalPrice)
            product_dic['total'] = float(order.totalPrice)
            product_list = list(order.products.all())
            product_dic['products'] = product_list
            # print("%%%%%%%%%% product_dic: ", product_dic)
            order_dic[str(order.pk)] = product_dic

            # order_dic[str(order.pk)] = product_list
        context_dict['allorders'] = order_dic
        print("######### allorders::", order_dic)

    # orderlist=list(all_orders.all())
    # price_dic={}
    # for i in orderlist:
    #     price_dic[str(i.pk)] = i.totalPrice
    # context_dict['totalPrice'] = price_dic
    # print("\n\nTotal price dict\n",context_dict['totalPrice'],"\n\n")

    # print("\n\nFull dictionary:\n",context_dict,"\n\n")
    context_dict['username'] = request.user.username
    context_dict['money'] = profile.balance
    #context_dict['all_orders'] = all_orders
    #print("\n\n",all_orders,"\n\n")
    #context_dict['totalPrice'] = all_orders.totalPrice
    check_vip(profile)

    if "rating" in request.POST:
        rating_input = request.POST['rating']
        listed_product_pk = request.POST['product_pk']
        prod = Product.objects.get(pk= listed_product_pk)
        listed_seller = prod.seller
        user_seller = User.objects.get(username = listed_seller)
        seller_profile = UserProfile.objects.get(user = user_seller)

        r = Rating.objects.get_or_create(user = seller_profile, rated_by = profile, product = prod)[0]
        r.rating = int(rating_input)
        # new_rating = Rating(user=seller_profile,rating = int(rating_input), rated_by = profile, product = prod)
        r.save()
        update_rating(seller_profile)
        check_rater(profile)
    return render(request, 'orders.html', context_dict)


def check_rater(rater_profile):
    sr = Rating.objects.filter(rated_by = rater_profile).order_by('-id')[:5]
    sr_list = list(sr.values_list('rating',flat = True))

    if len(sr_list) >= 3:
        if sr_list.count(1) == 3:
            rater_profile.strikes += 1
            rater_profile.save()
            print ('strikes          ', rater_profile.strikes)

    if len(sr_list)>= 5:
        if sr_list.count(5) == 5:
            rater_profile.strikes += 1
            rater_profile.save()