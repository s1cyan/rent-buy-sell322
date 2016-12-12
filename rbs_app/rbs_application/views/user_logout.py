from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from ..date_checker import update_all


# @login_required
def user_logout(request):
    update_all()
    logout(request)
    # Redirect to visitor home page
    return HttpResponseRedirect(reverse('index'))