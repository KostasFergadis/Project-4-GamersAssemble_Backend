from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
User = get_user_model()


class JWTAuthentication(BasicAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        if not auth_header.startswith('Bearer '):
            raise PermissionDenied(detail="Invalid Auth Token Format")

        token = auth_header.replace('Bearer ', "")
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(pk=int(payload.get('sub')))

        except jwt.exceptions.InvalidTokenError:
            raise PermissionDenied(detail='Invalid Token')

        except (User.DoesNotExist, TypeError, ValueError):
            raise PermissionDenied(detail='User Not Found')

        return (user, token)

    def authenticate_header(self, request):
        # Without this DRF inherits "Basic" from BasicAuthentication, which makes
        # browsers show a native username/password prompt on every 401.
        return 'Bearer'
