from django.urls import path, include
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import requests

from rest_framework import serializers, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from django.core import signing

from .serializers import UserSerializer, UserSignUpSerializer, UserSignInSerializer
from .permissions import IsUserOrReadOnly, CanOnlyCreateOrDeleteOrUpdate

from lan_papascal.settings import CLIENT_ID, CLIENT_SECRET, BASE_URL

class UserList(generics.ListAPIView):
    permission_classes = [CanOnlyCreateOrDeleteOrUpdate, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveUpdateAPIView):
    permission_classes = [IsUserOrReadOnly, TokenHasReadWriteScope]
    serializer_class = UserSerializer

    def get_queryset(self):
        email = self.request.user.email
        return User.objects.filter(email = email)

class SignUp(generics.GenericAPIView):
    serializer_class = UserSignUpSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format = None):
        '''
        Registers user to the server. Input should be in the format:
        {"username": "username", "password": "1234abcd"}
        '''
        serializer = UserSignUpSerializer(data = request.data)

        if serializer.is_valid(): 
           
            r = requests.post(f'{BASE_URL}/o/token/', 
                data = {
                    'grant_type': 'password', 
                    'username': request.data['username'], 
                    'password': request.data['password'], 
                    'client_id': CLIENT_ID, 
                    'client_secret': CLIENT_SECRET, 
                }, 
            ) 

            serializer.save()

            return Response(r.json(),status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    serializer_class = UserSignInSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format = None):
        '''
        Gets tokens with username and password. Input should be in the format:
        {"username": "username", "password": "1234abcd"}
        '''
        r = requests.post(f'{BASE_URL}/o/token/', 
            data = {
                'grant_type': 'password', 
                'username': request.data['username'], 
                'password': request.data['password'], 
                'client_id': CLIENT_ID, 
                'client_secret': CLIENT_SECRET, 
            }, 
        )

        encrypted = signing.dumps(r.json())
        resp = Response(status=status.HTTP_201_CREATED)
        resp.set_cookie("access",encrypted, samesite="Strict", max_age=1800)
        return resp

class RefreshToken(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format = None):
        '''
        Registers user to the server. Input should be in the format:
        {"refresh_token": " < token > "}
        '''
        r = requests.post(
        f'{BASE_URL}/o/token/', 
            data = {
                'grant_type': 'refresh_token', 
                'refresh_token': request.data['refresh_token'], 
                'client_id': CLIENT_ID, 
                'client_secret': CLIENT_SECRET, 
            }, 
        )
        return Response(r.json())


class RevokeToken(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format = None):
        '''
        Method to revoke tokens.
        {"token": " < token > "}
        '''
        r = requests.post(
            f'{BASE_URL}/o/revoke_token/', 
            data = {
                'token': request.data['token'], 
                'client_id': CLIENT_ID, 
                'client_secret': CLIENT_SECRET, 
            }, 
        )
        # If it goes well return success message (would be empty otherwise) 
        if r.status_code == request.codes.ok:
            return Response({'message': 'token revoked'}, r.status_code)
        # Return the error if it goes badly
        return Response(r.json(), r.status_code)