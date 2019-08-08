from django.urls import path, include

from .views import SignUpView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name="sign-up"),
    path('password/change/', PasswordChangeView.as_view(), name="password-change"),
    path('password/reset/', PasswordResetView.as_view(), name="password-reset"),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name="password-reset-confirm")
]