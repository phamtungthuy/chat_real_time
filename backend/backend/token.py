from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import inline_serializer, OpenApiResponse
from rest_framework import serializers

@extend_schema(
    tags=['Authentication Token'],
    summary="Get authentication token of a particular user",
    description="This token is necessary for private actions\n\n"
    "Your account need to be verified through email before getting authentication token",
    request=inline_serializer(
        name="TokenObtainPairViewSerializer",
        fields={
            "username": serializers.CharField(),
            "password": serializers.CharField()
        }
    ),
    responses={
        200: OpenApiResponse(response=inline_serializer(
            name="SuccessResponseTokenObtainPairViewSerializer",
            fields={
                "access": serializers.CharField(),
                "refresh": serializers.CharField()
            },
            
        ), description="Success getting authentication token"),
        401: OpenApiResponse(response=inline_serializer(
            name="FailedResponseTokenObtainPairViewSerializer",
            fields={
                "detail": serializers.CharField()
            },
           
        ),  description="Account is not found or verified")
    }
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(
    tags=['Authentication Token'],
    summary="Refresh authentication token of a particular user",
    description="Your token can be out of date\n\n"
    "This api will help you make new token",
    request=inline_serializer(
        name="TokenRefreshViewSerializer",
        fields={
            "refresh": serializers.CharField()
        }
    ),
    responses={
        200: OpenApiResponse(response=inline_serializer(
            name="SuccessResponseTokenRefreshViewSerializer",
            fields={
                "access": serializers.CharField(),
                "refresh": serializers.CharField()
            },
            
        ), description="Success refreshing authentication token"),
        401: OpenApiResponse(response=inline_serializer(
            name="FailedResponseTokenRefreshViewSerializer",
            fields={
                "detail": serializers.CharField(),
                "code": serializers.CharField()
            },
            
        ), description="Token is in valid or expired")
    }
)
class CustomTokenRefreshView(TokenRefreshView):
    pass
