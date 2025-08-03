from django.http import HttpResponseForbidden
from functools import wraps

# ✅ Admin only (role-based, not superuser)
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Admins only")
    return _wrapped_view

# ✅ Staff and Admin roles
def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in ['admin', 'staff']:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Staff/Admins only")
    return _wrapped_view
