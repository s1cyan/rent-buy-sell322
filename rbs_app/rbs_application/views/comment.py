from django.shortcuts import render
from ..models import Comment, Product, UserProfile

def comment(request):
    """Visitors and users can write comments on a product."""
    profile = UserProfile.objects.get(user=request.user)
    product_pk = request.POST.get('pk','')
    product = Product.objects.get(pk = product_pk)
    all_comments = Comment.objects.filter(product=product)
    context_dict = {
        'username': request.user.username,
        'money': profile.balance,
    }
    context_dict['all_comments'] = all_comments
    print("hello")
    print(request.method)
    if request.method == "POST":
        # print("we made it")
        comment = request.POST.get('text')
        # print(comment)
        comment = Comment(text=comment, product=product)
        comment.save()
        context_dict = {
            'text': all_comments,
        }
        return render(request, 'item-details.html', context_dict)
    return render(request,'item-details.html', context_dict)