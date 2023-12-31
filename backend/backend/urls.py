from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView 
from .token import CustomTokenObtainPairView, CustomTokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html')),
    #path('', TemplateView.as_view(template_name='index.html')),
    #path('admin/', TemplateView.as_view(template_name='index.html')),
    #path('signup/', TemplateView.as_view(template_name='index.html')),
    #path('signin/', TemplateView.as_view(template_name='index.html')),
    #path('reset-password/', TemplateView.as_view(template_name='index.html')),
 
    path('doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),
    # path('silk/', include('silk.urls', namespace='silk')),
    path('chat/', include('chat.urls')),

    path('api/channel/', include('channel.urls')),
    path('api/message/', include('message.urls')),
    path('api/user/', include('user.urls')),
    path('api/report/', include('report.urls')),
    path('api/search/', include('search.urls')),
    
    # path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]