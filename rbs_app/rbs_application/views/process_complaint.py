from django.contrib.auth.models import User
from django.shortcuts import render
from ..models import Complaint, UserProfile


def process_complaint(request):
    '''
    *** Put the functions to process complaints and send them to db here - same method as the others
    do request.POST['name value in template'] to access values
    Users can submit a complaint for a user, if they get the username wrong
    users will be told they submitted a complaint, but it will not necessarily be registered
    bc the user has to be in our system
    :param request:
    :return:
    '''
    profile= UserProfile.objects.get(user=request.user)
    context_dict = {
        'username': request.user.username,
        'money': profile.balance,
    }
    if User.objects.filter(username=request.POST['reported_user']).exists():
        complained_user = User.objects.get(username = request.POST['reported_user'])
        complaint_user_profile = UserProfile.objects.get(user = complained_user)
        complaint_str = request.POST['complaint']
        complaint = Complaint( user_id = complaint_user_profile,
                               complaint = complaint_str)
        complaint.save()
    return render(request,'complaint-submitted.html', context_dict)