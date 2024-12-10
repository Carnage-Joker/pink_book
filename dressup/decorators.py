# dressup/decorators.py

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def avatar_required(function):
    @login_required
    def wrap(request, *args, **kwargs):
        if not hasattr(request.user, 'avatar'):
            return redirect('dressup:create_avatar')
        else:
            return function(request, *args, **kwargs)
    return wrap
