from django.shortcuts import render
from ..models import UserProfile
from ..date_checker import update_all

def index(request):
    """Redirect to home page

    Populates username and balance is user is authenticated.
    Else, shows generic homepage for visitor.
    """
    update_all()
    context_dict = dict()
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        context_dict['username'] = request.user.username
        context_dict['money'] = profile.balance
    return render(request, 'index.html', context_dict)