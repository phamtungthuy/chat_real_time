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
        200: OpenApiResponse(response=SuccessGetChannelListSerializer, description="Get all joined channels successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need to be authorized before making this action"),
    }
)

getUserProfileSchema = extend_schema(
    summary="Get detail information of a user",
    description="You need authentication token of current user to get user's profile \n\n \
    You can access to profile of almost all users except for special users such as admins",
    responses = {
        200: OpenApiResponse(response=SuccessGetUserProfileSerializer, description="Get a particular user profile successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need provide authentication token to make this action"),
        404: OpenApiResponse(response=GeneralMessageSerializer, description="User profile not found")
    }
)

updateUserProfileSchema = extend_schema(
    summary = "Update current user's profile information",
    description ="You need authentication token of current user to update profile",
    request=UserProfileSerializer,
    responses= {
        200: OpenApiResponse(response = SuccessUpdateUserProfileSerializer, description="Update user profile successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need provide authentication token to make this action"),
        400: OpenApiResponse(response=GeneralMessageSerializer, description="There are some problems when making this action")
    }
)

uploadUserAvatarSchema = extend_schema(
    summary= "Upload current user's avatar",
    description="You need authentication token of current user to upload avatar\n\n"
                "Please send file using multipart/form-data",
    request= FileUploadSerializer,
    responses = {
        200: OpenApiResponse(response=SuccessUploadAvatarSerializer, description="Upload Avatar successfully"),
        400: OpenApiResponse(response=GeneralMessageSerializer, description="File is not provided"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need provide authentication token to make this action"),
        413: OpenApiResponse(response=GeneralMessageSerializer, description="Size of data is too large"),
        415: OpenApiResponse(response=GeneralMessageSerializer, description="Unsupported media type"),   
        
    }
)

getFriendListSchema = extend_schema(
    summary = "Get friend list of current user",
    description="You need authentication token of current user to get friend list",
    responses = {
        200: OpenApiResponse(response=SuccessGetFriendListSerializer, description="Get friend list successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need provide authentication token to make this action"),
        
    }
)

deleteFriendSchema = extend_schema(
    summary= "Delete a particular friend from friend list",
    description="You need authentication token of current user to delete user's friend",
    responses = {
        200: OpenApiResponse(response=GeneralMessageSerializer, description="Delete friend successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need provide authentication token to make this action"),
        404: OpenApiResponse(response=GeneralMessageSerializer, description="Friend not found")
    }
)

getNotificationListSchema = extend_schema(
    summary = "Get all notifications of current user",
    description="You need authentication token of current user to get all notifications",
    responses = {
        200: OpenApiResponse(response=SuccessGetNotificationListSerializer, description="Get notification list successfully"),
        401: OpenApiResponse(response=GeneralMessageSerializer, description="You need provide authentication token to make this action"),
        
    }

)