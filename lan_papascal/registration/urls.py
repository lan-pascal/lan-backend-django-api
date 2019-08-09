from django.urls import path, include

from django.contrib.auth import views

urlpatterns = [
    path('signin/', views.LoginView.as_view(template_name='registration/signin.html'), name='signin'),
    path('signout/', views.LogoutView.as_view(template_name='registration/signout.html'), name='signout'),

    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path(
        'password/reset/', 
        views.PasswordResetView.as_view(
            email_template_name='registration/email/password_reset_body.html', 
            subject_template_name='registration/email/password_reset_subject.txt'
            ), 
        name='password_reset'
    ),
    path('password/reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
