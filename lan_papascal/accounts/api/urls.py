from django.urls import path, include

from .views import UserList, UserDetails, SignIn, SignUp, RefreshToken, RevokeToken

urlpatterns = [
    #Accounts API
    path('users/', UserList.as_view()),
    path('users/<username>/', UserDetails.as_view()),

    #Proxy Server/Authorization Server
    path('signin/', SignIn.as_view()),
    path('signup/', SignUp.as_view()),
    path('refresh_token/', RefreshToken.as_view()),
    path('revoke_token/', RevokeToken.as_view()),
]
