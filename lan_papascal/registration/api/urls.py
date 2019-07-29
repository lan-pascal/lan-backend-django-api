from django.urls import path, include

from .views import SignInView, SignUpView, RefreshTokenView, RevokeTokenView


urlpatterns = [
    path('signin/', SignInView.as_view(), name="sign-in"),
    path('signup/', SignUpView.as_view(), name="sign-up"),
    path('refresh_token/', RefreshTokenView.as_view(), name="refresh-token"),
    path('revoke_token/', RevokeTokenView.as_view(), name="revoke-token"),
]