from django.urls import path
from .views import ReportViewSet

urlpatterns = [
    path('', ReportViewSet.as_view({
        'post': 'createReport',
    })),
    path('<int:reportId>/', ReportViewSet.as_view({
        'get': 'getReportDetail',
        'put': 'processReport',
        'delete': 'deleteReport'
    })),
    path('channel/', ReportViewSet.as_view({
        'get': 'getReportedChannel',
    })),
    path('user/', ReportViewSet.as_view({
        'get': 'getReportedUser',
    }))
]
