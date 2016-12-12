from django.shortcuts import redirect
from ..date_checker import update_all


def redir(request):
    # TODO redirection for top nav bar
    update_all()
    return redirect('/rbs')
