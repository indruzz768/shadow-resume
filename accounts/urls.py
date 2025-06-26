from django.urls import path
from . import views
# urls.py
from .views import toggle_staff

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-profile/', views.profile_edit, name='profile_edit'),
    path('profile/', views.profile_view, name='profile'),
    path('admin/users/<int:user_id>/toggle/', toggle_staff, name='toggle_staff'),

]
