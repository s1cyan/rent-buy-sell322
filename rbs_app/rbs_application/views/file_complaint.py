from django.shortcuts import render, redirect
from ..forms import ComplaintForm
from ..models import UserProfile

def file_complaint(request):
    """"""
    complaint_form = ComplaintForm(request.POST)
    profile= UserProfile.objects.get(user=request.user)
    context_dict = {
        'username': request.user.username,
        'money':profile.balance,
        'complaint-form': complaint_form,
        'process_complaint': '/rbs/submitted-complaint',
    }

    return render(request, 'file-complaint.html', context_dict)