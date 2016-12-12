from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..forms import SellForm
from ..models import UserProfile
from ..date_checker import update_all


@login_required
def sell_item(request):
    '''
    :param request:
    :return:
    has the sell form, sends the return values to process the request at function process_sell()
    '''
    sell_form = SellForm(request.POST)
    profile = UserProfile.objects.get(user=request.user)
    context_dict = {
        'username': request.user.username,
        'money': profile.balance,
        'sell_form': sell_form,
        'process_sell_post': '/rbs/process-listing'
    }
    update_all()
    return render(request, 'sell-item.html', context_dict)