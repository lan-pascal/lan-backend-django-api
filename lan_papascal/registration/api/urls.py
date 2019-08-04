from django.urls import path, include

from .views import SignInView, SignUpView, RefreshTokenView, RevokeTokenView, PasswordChangeView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView


urlpatterns = [
    path('signin', SignInView.as_view(), name="sign-in"),
    path('signup', SignUpView.as_view(), name="sign-up"),
    path('refresh_token', RefreshTokenView.as_view(), name="refresh-token"),
    path('revoke_token', RevokeTokenView.as_view(), name="revoke-token"),
    path('password/change', PasswordChangeView.as_view(), name="password-change"),
    path('password/reset', PasswordResetView.as_view(), name="password-reset"),
    path('password/reset/confirm', PasswordResetConfirmView.as_view(), name="password-reset-confirm")
]