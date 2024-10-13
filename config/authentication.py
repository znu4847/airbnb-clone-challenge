from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class UsernameAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.headers.get("X-USERNAME")
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found.")
        return (user, None)
