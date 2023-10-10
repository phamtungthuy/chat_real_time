from django.urls import path
from .views import ReportViewSet

urlpatterns = [
    path('channel/', ReportViewSet.as_view({
        'get': 'getReportedChannel',
    })),
    path('user/', ReportViewSet.as_view({
        'get': 'getReportedUser',
    }))
]
