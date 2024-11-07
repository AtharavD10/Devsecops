from django.urls import path
from .views import index, contact, login_view, register_view, logout_view
from django.shortcuts import redirect
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', lambda request: redirect('main') if request.user.is_authenticated else redirect('login'), name='root'),  # Redirect root URL to login
    path('main/', index, name='main'),  # Main page, protected by login
    path('contact/', contact, name='contact'),  # Contact page
    path('login/', login_view, name='login'),  # Login page
    path('register/', register_view, name='register'),  # Registration page
    path('diet/view/<int:diet_id>/', views.view_diet, name='view_diet'),
    path('diet/edit/<int:diet_id>/', views.edit_diet, name='edit_diet'),
    path('logout/', logout_view, name='logout'), 
]
