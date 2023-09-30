from django.contrib.auth.models import AnonymousUser, User
from rest_framework_simplejwt.tokens import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from jwt import decode
from jwt.exceptions import DecodeError, ExpiredSignatureError
from django.conf import settings

@database_sync_to_async
def get_user(decoded_token):
    try:
        user = User.objects.get(id=decoded_token["user_id"])        
        return user
    except User.DoesNotExist:
        return AnonymousUser()

class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            token = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
            decoded_token = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except (ValueError, DecodeError, ExpiredSignatureError) as e:
            token = None
            # print(e)
        scope['user'] = AnonymousUser() if token is None else await get_user(decoded_token)
        return await super().__call__(scope, receive, send)

def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))