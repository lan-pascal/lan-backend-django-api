from django.urls import path, include

from django.contrib.auth import views as django_views
from . import views

urlpatterns = [
    #Basic
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signout/', django_views.LogoutView.as_view(template_name='registration/signout.html'), name='signout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/done', views.SignUpDoneView.as_view(),  name="signup_done"),

    path(
        'password_reset/', 
        django_views.PasswordResetView.as_view(
            email_template_name='registration/email/password_reset_body.html', 
            subject_template_name='registration/email/password_reset_subject.txt'
            ), 
        name='password_reset'
    ),
    path('password_reset/done/', django_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', django_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', django_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
