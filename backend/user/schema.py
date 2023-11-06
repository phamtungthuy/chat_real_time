from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from message.serializer import MessageSerializer
from .serializer import UserSerializer
from .schemaSerializer import *
signUpSchema = extend_schema(
    summary="Sign up a new user account",
    request=UserSerializer,
    responses = {
        200: OpenApiResponse(response=SuccessSignUpSerializer, description='Operations successfully'),
        400: OpenApiResponse(response=GeneralMessageSerializer, description='Bad Request')
    }
)

loginSchema = extend_schema(
    summary="Login after verified",
    request = UserLoginSerializer,
    responses = {
        200: OpenApiResponse(response=SuccessUserLoginSerializer, description="Operations when login successfully!"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="User is not unauthorized"),
        403: OpenApiResponse(response=GeneralMessageSerializer, description="User is banned"),
        404: OpenApiResponse(response=GeneralMessageSerializer, description="User not found")
    }
)

verifyEmailSchema = extend_schema(
    summary="Verify after receiving a verification code from email",
    request=verifyEmailSerializer,
    responses = {
        200: OpenApiResponse(response=GeneralMessageSerializer, description="Verified successfully!"),
        400: OpenApiResponse(response=GeneralMessageSerializer, description="Bad request"),
        404: OpenApiResponse(response=GeneralMessageSerializer, description="User not found")
    }
)

resendVerificationSchema = extend_schema(
    summary="Resend verification code if having some problems with previous code",
    request=ResendVerificationSerializer,
    responses= {
        200: OpenApiResponse(response=SuccessResendVerificationCode, description="Resend code successfully"),
        400: OpenApiResponse(response=GeneralMessageSerializer, description="Bad request"),
        404: OpenApiResponse(response=GeneralMessageSerializer, description="User not found")
    }
)

getAllUsersSchema = extend_schema(
    summary="Get All Users if have permission",
    description="If you want to get all users, you need permission, normal users can not get information of all users",
    responses = {
        200: OpenApiResponse(response=SuccessGetAllUsersSerializer, description="Get all users successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need to be authorized before making this action"),
        403: OpenApiResponse(response=GeneralMessageSerializer, description="You don't have permission to get all users")
    }
)

banUserSchema = extend_schema(
    summary="Ban user if have permission",
    description="You need permission to ban users, normal users can not ban users",
    responses = {
        200: OpenApiResponse(response=GeneralMessageSerializer, description="User is banned"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need to be authorized before making this action"),
        403: OpenApiResponse(response=GeneralMessageSerializer, description="You don't have permission to ban users")
    }
)

getChannelListSchema = extend_schema(
    summary="Get all channels which current user are joining in",
    description="You need authentication token to get all channels",
    responses = {
        200: OpenApiResponse(response=SuccessGetChannelListSerializer, description="get all joined channels successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need to be authorized before making this action"),
    }
)