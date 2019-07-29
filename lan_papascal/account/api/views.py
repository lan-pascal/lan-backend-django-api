from django.contrib.auth import get_user_model, authenticate
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import requests

from rest_framework import serializers, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from ..conf import settings

from .serializers import UserSerializer, UserSignUpSerializer, UserSignInSerializer
from .permissions import IsUserOrReadOnlyIfPublic

User = get_user_model()

class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser & TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetails(generics.RetrieveUpdateAPIView):
    permission_classes = [IsUserOrReadOnlyIfPublic & TokenHasReadWriteScope]
    serializer_class = UserSerializer(partial_update=True)
    queryset = User.objects.all()
    lookup_field = "username"