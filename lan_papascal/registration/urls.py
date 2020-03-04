from django.urls import path, include
from django.views.generic import TemplateView

from django.contrib.auth import views as django_views
from django_registration.backends.activation import views as django_registration_views

from . import views
from . import forms

urlpatterns = [
    #Plugins
    path(
        "register/",
        django_registration_views.RegistrationView.as_view(form_class=forms.RegistrationForm),
        name="django_registration_register",
    ),
    path('',include('django_registration.backends.activation.urls')),
    
    #Basic
    path('signin/', django_views.LoginView.as_view(template_name='registration/signin.html',redirect_authenticated_user=True), name='signin'),
    path('signout/', django_views.LogoutView.as_view(template_name='registration/signout.html'), name='signout'),
    
    path('password_change/', django_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', django_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path(
        'password_reset/', 
        django_views.PasswordResetView.as_view(
            email_template_name='registration/email/password_reset_body.html', 
            subject_template_name='registration/email/password_reset_subject.txt'
            ), 
        name='password_reset'
    ),
    path('password_reset/done/', django_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/', django_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', django_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
