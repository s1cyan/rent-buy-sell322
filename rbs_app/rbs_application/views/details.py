from django.shortcuts import render
from ..associate import associate_option
from ..models import Comment, Product, UserProfile
from ..date_checker import update_all


def details(request):
    update_all()
    # View for clicking 'View item details' in search results
    context_dict = dict()
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        context_dict['username'] = request.user.username
        context_dict['money'] = profile.balance
    # Check if VIEW DETAILS button was pressed
    if "view_details" in request.POST:
        product_pk = request.POST['view_details']
        product = Product.objects.get(pk=product_pk)
        comments = Comment.objects.filter(product=product)
        context_dict['product'] = product
        context_dict['option'] = associate_option(product.option)
        context_dict['product_pk'] = product_pk
        context_dict['product_id'] = product.id
        context_dict['comments'] = comments

    # Check if ADD A COMMENT button was pressed
    if "add_comment" in request.POST:
        product_pk = request.POST['add_comment']
        product = Product.objects.get(pk=product_pk)
        context_dict['product'] = product
        context_dict['option'] = associate_option(product.option)
        context_dict['description'] = product.text
        context_dict['product_pk'] = product_pk
        context_dict['product_id'] = product.id
        new_comment = Comment(product=product, text=request.POST['new_comment'])
        new_comment.save()
        comments = Comment.objects.filter(product=product)
        context_dict['comments'] = comments
        print("ADD A COMMENT BUTTON was pressed for product_pk:", product_pk)
        print("NEW COMMENT:", new_comment)
        return render(request, "item-details.html", context_dict)

    if product.option == Product.AUCTION:
        # return auction_item_details_users(request,context_dict)
        return render(request, 'auction_details.html', context_dict)

    # else:
    return render(request, 'item-details.html', context_dict)
