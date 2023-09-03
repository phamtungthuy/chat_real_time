from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, inline_serializer
from drf_spectacular.types import OpenApiTypes
from .serializers import UserSerializer
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):    
    @extend_schema(
        responses={
            200: OpenApiResponse(response=UserSerializer,
                                 description="Operations successfully")
        }
        # more customizations
    )

    def retrieve(self, request, id=None, username=None):
        try:
            if id is None:
                user = User.objects.get(username=username)
            else:
                user = User.objects.get(id=id)
            serializer = UserSerializer(user)
        except User.DoesNotExist:
            return Response({'message': f'User not found - {id} - {username}'},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
         request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "required": True},
                    "password": {"type": "string"},
                    "email": {"type": "string"}},
            },
        },
    )
    
    def create(self, request):
        data = request.data
        if any(field not in data for field in ['username', 'email', 'password']):
            return Response({
                'message': 'username, email and password must be provided',
                }, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Account created successfully'},status=status.HTTP_200_OK)
        message = ""
        for key, value in serializer.errors.items():
            message += value[0]
            break
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, id=None, username=None):
        pass
    
    def delete(self, request, id=None, username=None):
        pass
    