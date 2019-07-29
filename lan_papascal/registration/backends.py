from django.contrib.auth import backends, get_user_model
from django.db.models import Q

User = get_user_model()


class AccountsBackend(backends.ModelBackend):

    def authenticate(self, request,**credentials):
        username = credentials["username"]
        email = credentials["email"]
        password = credentials["password"]
        
        if username is None or email is None or password is None:
            return
        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=email))
        except User.DoesNotExist:
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user