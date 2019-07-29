from django.urls import path, include

from .views import UserList, UserDetails, SignIn, SignUp, RefreshToken, RevokeToken

urlpatterns = [
    #Accounts API
    path('users/', UserList.as_view(), name="users-list"),
    path('users/<str:username>/', UserDetails.as_view(), name="users-details"),
]
