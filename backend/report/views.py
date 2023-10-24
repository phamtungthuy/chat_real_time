from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Report
from .serializer import ReportSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Report'])
class ReportViewSet(viewsets.ViewSet):
    query_set = Report.objects.all()
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.action == 'createReport':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


    def getReportedChannel(self, request):
        reportedChannels = self.query_set.filter(report_type="REPORT_CHANNEL")
        serializer = self.serializer_class(reportedChannels, many=True)
        return Response({"message": "Get reported channels successfully", "data": serializer.data})


    def getReportedUser(self, request):
        reportedUsers = self.query_set.filter(report_type="REPORT_USER")
        serializer = self.serializer_class(reportedUsers, many=True)
        return Response({"message": "Get reported users successfully", "data": serializer.data})


    def createReport(self, request):
        data = request.data.copy()
        data['reporter'] = request.user.id
        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Create report successfully", "data": serializer.data})
        message = ""
        for key, value in serializer.errors.items():
            message += f'{value[0]} ({key})'
            break
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


    def getReportDetail(self, request, reportId):
        try:
            report = self.query_set.get(pk=reportId)
            serializer = self.serializer_class(report, many=False)
            return Response({"message": "Get report detail successfully", "data": serializer.data})
        except:
            return Response({"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)


    def processReport(self, request, reportId):
        try:
            report = self.query_set.get(pk=reportId)
            report.processed = True
            report.save()
            return Response({"message": "Process report successfully"})
        except:
            return Response({"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)


    def deleteReport(self, request, reportId):
        try:
            report = self.query_set.get(pk=reportId)
            report.delete()
            return Response({"message": "Delete report successfully"})
        except:
            return Response({"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)