from rest_framework.response import Response
from rest_framework import viewsets
from .models import Report
from .serializer import ReportSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated

class ReportViewSet(viewsets.ViewSet):
    query_set = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def getReportedChannel(self, request):
        return Response('oke')


    def getReportedUser(self, request):
        return Response('oke')
