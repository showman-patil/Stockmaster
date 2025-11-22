from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import EmailOrUsernameAuthenticationForm

urlpatterns = [
    # Use Django's built-in LoginView with a custom form that accepts email or username
    path('', auth_views.LoginView.as_view(template_name='login.html', authentication_form=EmailOrUsernameAuthenticationForm), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export/', views.export_report, name='export_report'),
    path('profile/', views.profile_view, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    # Password reset (using Django auth views)
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
