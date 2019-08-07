from django.contrib.auth import get_user_model

from rest_framework import generics, views
from rest_framework.response import Response

from . import serializers
from ..conf import settings

def _get_serializer(self, *args, **kwargs):
    serializer_class =  self.serializer_class
    kwargs["context"] = {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
    }
    return serializer_class(*args,**kwargs)

class SignUp(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()

    queryset = get_user_model().objects.all()
    serializer_class = serializers.SignUpSerializer

class PasswordChangeView(views.APIView):
    permisssion_classes = ()

    serializer_class = serializers.PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = _get_serializer(self,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": ("Your password has been change successfuly.")}
        )

class PasswordResetView(views.APIView):
    permisssion_classes = ()

    serializer_class = serializers.PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = _get_serializer(self,data=request.data)
        serializer.is_valid(raise_exception=False)
        serializer.save()
        return Response(
            {"detail": ("We have send you an email to reset your password.")}
        )

class PasswordResetConfirmView(views.APIView):
    permisssion_classes = ()

    serializer_class = serializers.PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = _get_serializer(self,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": ("Your password has been reset with the new password.")}
        )