from django_rest_passwordreset.serializers import PasswordTokenSerializer
from django_rest_passwordreset.views import ResetPasswordValidateTokenViewSet, ResetPasswordConfirmViewSet, \
    ResetPasswordRequestTokenViewSet
    
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Reset Password'])
class CustomResetPasswordRequestTokenViewSet(ResetPasswordRequestTokenViewSet):
    pass

@extend_schema(tags=['Reset Password'])
class CustomResetPasswordConfirmViewSet(ResetPasswordConfirmViewSet):
    pass

@extend_schema(tags=['Reset Password'])
class CustomResetPasswordValidateTokenViewSet(ResetPasswordValidateTokenViewSet):
    pass

