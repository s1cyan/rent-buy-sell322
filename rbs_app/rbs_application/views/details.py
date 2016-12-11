from django.shortcuts import render
from ..associate import associate_option
from ..models import Comment, Product, UserProfile


def details(request):
    # View for clicking 'View item details' in search results
    context_dict = dict()
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        context_dict['username'] = request.user.username
        context_dict['money'] = profile.balance
    product_pk = request.POST.get('pk', '')
    product = Product.objects.get(pk=product_pk)
    comments = Comment.objects.filter(product=product)
    # print("\n\n\n\nCOMMENTS FOR SKYLINES", comments)
    context_dict['item'] = product.title
    context_dict['price'] = product.price
    context_dict['seller'] = product.seller.username
    context_dict['option'] = associate_option(product.option)
    context_dict['description'] = product.text
    context_dict['product_pk'] = product_pk
    context_dict['product_id'] = product.id
    context_dict['date'] = product.takedown_date
    context_dict['time'] = product.takedown_time
    context_dict['comments'] = comments
    if product.option == Product.AUCTION:
        # return auction_item_details_users(request,context_dict)
        return render(request, 'auction_details.html', context_dict)

    # else:
    return render(request, 'item-details.html', context_dict)
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
            # return render(request,'item-details.html',context_dict)
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