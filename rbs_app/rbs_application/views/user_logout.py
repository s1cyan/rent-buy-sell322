from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


# @login_required
def user_logout(request):
    logout(request)
    # Redirect to visitor home page
    return HttpResponseRedirect(reverse('index'))