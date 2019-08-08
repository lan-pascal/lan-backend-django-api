from django.urls import path, include

from .views import SignUpView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name="sign_up"),
    path('password/change/', PasswordChangeView.as_view(), name="password_change"),
    path('password/reset/', PasswordResetView.as_view(), name="password_reset"),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name="password_reset_confirm")
]