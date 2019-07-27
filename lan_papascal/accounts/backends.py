from django.contrib.auth import backends, get_user_model
from django.db.models import Q

User = get_user_model()


class AccountsBackend(backends.ModelBackend):

    def authenticate(self, request, identification=None, password=None, **kwargs):
        
        if identification is None:
            identification = kwargs.get(User.USERNAME_FIELD)
        if identification is None or password is None:
            return
        try:
            user = User.objects.get(Q(username__iexact=identification) | Q(email__iexact=identification))
        except User.DoesNotExist:
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user