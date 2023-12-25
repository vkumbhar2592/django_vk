from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view
