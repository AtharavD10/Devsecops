from django.urls import path
from django.shortcuts import redirect
from .views import index, contact, login_view, register_view, logout_view
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Root URL redirects to main if authenticated, otherwise to login
    path('', lambda request: redirect('main') if request.user.is_authenticated else redirect('login'), name='root'),

    # Main pages
    path('main/', index, name='main'),  # Main page, protected by login
    path('contact/', contact, name='contact'),  # Contact page
    path('login/', login_view, name='login'),  # Login page
    path('register/', register_view, name='register'),  # Registration page
    path('logout/', logout_view, name='logout'),  # Logout page

    # Diet-related views
    path('diet/view/<int:diet_id>/', views.view_diet, name='view_diet'),
    path('diet/edit/<int:diet_id>/', views.edit_diet, name='edit_diet'),
    path('diet/delete/<int:diet_id>/', views.delete_diet, name='delete_diet'),

    # Password reset views
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
