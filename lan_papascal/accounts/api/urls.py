from django.urls import path, include

from .views import UserList, UserDetails, SignIn, SignUp, RefreshToken, RevokeToken

urlpatterns = [
    #Accounts API
    path('users/', UserList.as_view(), name="users-list"),
    path('users/<str:username>/', UserDetails.as_view(), name="users-details"),

    #Proxy Server/Authorization Server
    path('signin/', SignIn.as_view(), name="sign-in"),
    path('signup/', SignUp.as_view(), name="sign-up"),
    path('refresh_token/', RefreshToken.as_view(), name="refresh-token"),
    path('revoke_token/', RevokeToken.as_view(), name="revoke-token"),
]
