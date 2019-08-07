from django.contrib.auth import get_user_model

from rest_framework.views import views
from rest_framework import generics
from rest_framework.response import Response

from . import serializers
from ..conf import settings

class SignUpView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()

    queryset = get_user_model().objects.all()
    serializer_class = serializers.SignUpSerializer

class PasswordChangeView(generics.GenericAPIView):
    permisssion_classes = ()

    serializer_class = serializers.PasswordChangeSerializer

    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": ("Your password has been change successfuly.")}
        )

class PasswordResetView(generics.GenericAPIView):
    permisssion_classes = ()

    serializer_class = serializers.PasswordResetSerializer

    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": ("We have send you an email to reset your password.")}
        )

class PasswordResetConfirmView(generics.GenericAPIView):
    permisssion_classes = ()

    serializer_class = serializers.PasswordResetConfirmSerializer

    def get_queryset():
        pass

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": ("Your password has been reset with the new password.")}
        )