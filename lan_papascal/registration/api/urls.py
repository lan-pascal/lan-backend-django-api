from django.urls import path, include

from .views import RegisterView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView


urlpatterns = [
    path('register', RegisterView.as_view(), name="sign-up"),
    path('password/change', PasswordChangeView.as_view(), name="password-change"),
    path('password/reset', PasswordResetView.as_view(), name="password-reset"),
    path('password/reset/confirm', PasswordResetConfirmView.as_view(), name="password-reset-confirm")
]