from django.shortcuts import render, redirect
from ..forms import ComplaintForm
from ..models import UserProfile
from ..date_checker import update_all


def file_complaint(request):
    update_all()
    """Handles Button: MAKE A COMPLAINT"""
    complaint_form = ComplaintForm(request.POST)
    context_dict = dict()
    context_dict['complaint-form'] = complaint_form
    context_dict['process_complaint'] = '/rbs/submitted-complaint'
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        context_dict['username'] = request.user.username
        context_dict['money'] = profile.balance
    # context_dict = {
    #     'username': request.user.username,
    #     'money':profile.balance,
    #     'complaint-form': complaint_form,
    #     'process_complaint': '/rbs/submitted-complaint',
    # }
    return render(request, 'file-complaint.html', context_dict)