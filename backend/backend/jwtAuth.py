from django.contrib.auth.models import AnonymousUser, User
from rest_framework_simplejwt.tokens import Token, TokenError
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from jwt import decode
from jwt.exceptions import DecodeError, ExpiredSignatureError
from django.conf import settings
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import TokenError

@database_sync_to_async
def get_user(decoded_token):
    try:
        user = User.objects.get(id=decoded_token["user_id"])        
        return user
    except User.DoesNotExist:
        return AnonymousUser()

@database_sync_to_async
def valid_token(decoded_token):
    if decoded_token['token_type'] != 'access':
        raise TokenError("Token type must be access key")
    jti = decoded_token['jti']
    if BlacklistedToken.objects.filter(token__jti=jti).exists():
        raise TokenError("Token is in black list")

class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            token = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
            decoded_token = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            await valid_token(decoded_token)
        except Exception as e:
            token = None
            print(e)
        scope['user'] = AnonymousUser() if token is None else await get_user(decoded_token)
        return await super().__call__(scope, receive, send)

def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))