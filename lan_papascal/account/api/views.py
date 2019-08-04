from django.contrib.auth import get_user_model

from rest_framework import serializers, generics, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .serializers import UserSerializer
from .permissions import IsUserOrReadOnlyIfPublic

User = get_user_model()

class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser & TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetails(generics.RetrieveUpdateAPIView):
    permission_classes = [IsUserOrReadOnlyIfPublic & TokenHasReadWriteScope]
    serializer_class = UserSerializer(partial=True)
    queryset = User.objects.all()
    lookup_field = "username"