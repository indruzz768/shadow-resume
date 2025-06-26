from django.http import HttpResponseForbidden

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Admins only")
    return _wrapped_view

def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role in ['admin', 'staff']:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Staff/Admins only")
    return _wrapped_view
