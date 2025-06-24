# departments/decorators.py
from django.http import HttpResponseRedirect
from django.urls import reverse

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))  # or a custom access denied page
    return wrapper_func
