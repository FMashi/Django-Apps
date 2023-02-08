from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views
from allauth.account.views import PasswordResetView



urlpatterns = [
    re_path(r'^accounts/register/$', views.user_register, name='register'),
    re_path(r'^accounts/login/$', views.login_user, name='login_user'),
    re_path(r'^accounts/login/e/$', views.login_email, name='login'),
    re_path(r'^accounts/login/p/$', views.login_password, name='login_password'),
    re_path(r'^accounts/$', views.profile, name='profile'),
    re_path(r'^accounts/settings/',views.edit_profile, name='edit_profile'),

    path('logout/', views.logout_view, name='logout'),

    # Change Password
    path('change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='commons/change-password.html',
            success_url = '/'
        ),
        name='change_password'
    ),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="user/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password/password_reset_complete.html'), name='password_reset_complete'),  
    #path("password_reset", views.password_reset_request, name="password_reset"),   
    re_path(r'^accounts/password_reset/$', views.password_reset_request, name='password_reset'), 



]