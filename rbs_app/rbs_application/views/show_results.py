from django.shortcuts import render
from ..models import Product, UserProfile


def show_results(request):
    # Searching for products is handled by this function
    context_dict = dict()
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        context_dict['username'] = request.user.username
        context_dict['money'] = profile.balance
    (query, method, min, max) = (request.GET['query'],
                                 request.GET['method'],
                                 request.GET['minprice'],
                                 request.GET['maxprice'], )
    results = Product.objects.filter(option=method, is_active=True)
    # print("ALL RESULTS: ", results)
    if query:  # TODO add logic to check for whitespace
        results = Product.objects.filter(title__icontains=query,
                                         option=method, is_active=True)
        (context_dict['results'], context_dict['found']) = (results, True)
        if not results:
            (context_dict['results'], context_dict['found']) = (results, False)
    else:
        (context_dict['results'], context_dict['found']) = (results, True)
    return render(request, 'results.html', context_dict)