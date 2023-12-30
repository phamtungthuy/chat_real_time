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
    })),
    path('all/', ReportViewSet.as_view({
        'get': 'getAllReports'
    })),
    path('recent/user/', ReportViewSet.as_view({
        'get': 'getRecentUserReports'
    })),
    path('recent/channel/', ReportViewSet.as_view({
        'get': 'getRecentChannelReports'
    })),
    path('recent/all/', ReportViewSet.as_view({
        'get': 'getRecentAllReports'
    })),
    path('stat/', ReportViewSet.as_view({
        'get': 'getAllReportsStat'
    })),
    path('recent/stat/', ReportViewSet.as_view({
        'get': 'getRecentAllReportsStat'
    }))
]
