from django.urls import path, include

from .views import SignIn, SignUp, RefreshToken, RevokeToken


urlpatterns = [
    path('signin/', SignIn.as_view(), name="sign-in"),
    path('signup/', SignUp.as_view(), name="sign-up"),
    path('refresh_token/', RefreshToken.as_view(), name="refresh-token"),
    path('revoke_token/', RevokeToken.as_view(), name="revoke-token"),
]