from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

@extend_schema(tags=['Token'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=['Token'])
class CustomTokenRefreshView(TokenRefreshView):
    pass
