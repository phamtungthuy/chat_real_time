from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Report
from .serializer import ReportSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_spectacular.utils import extend_schema
from .schema import *
from datetime import date, timedelta
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

    @getReportedChannelSchema
    def getReportedChannel(self, request):
        reportedChannels = self.query_set.filter(report_type="REPORT_CHANNEL")
        serializer = self.serializer_class(reportedChannels, many=True)
        return Response({"message": "Get reported channels successfully", "data": serializer.data})


    @getReportedUserSchema
    def getReportedUser(self, request):
        reportedUsers = self.query_set.filter(report_type="REPORT_USER")
        serializer = self.serializer_class(reportedUsers, many=True)
        return Response({"message": "Get reported users successfully", "data": serializer.data})

    def getAllReports(self, request):
        reports = self.query_set.all()
        serializer = self.serializer_class(reports, many=True)
        return Response({"message": "Get all reports successfully", "data": serializer.data})

    def getRecentUserReports(self, request):
        allReportedUsers = self.query_set.filter(report_type="REPORT_USER")
        reports = self.query_set.filter(create_at__gte=(date.today() - timedelta(days=7)), report_type="REPORT_USER")
        serializer = self.serializer_class(reports, many=True)
        allReportedUsersSerializer = self.serializer_class(allReportedUsers, many=True)
        percentage = 0
        if len(allReportedUsersSerializer.data) > 0:
            percentage = float(format(len(serializer.data) / len(allReportedUsersSerializer.data), ".4f"))
        return Response({"message": "Get recent reported users successfully", "data": {
            'data': serializer.data,
            'percentage': percentage
        }})
    
    def getRecentChannelReports(self, request):
        allReportedChannels = self.query_set.filter(report_type="REPORT_CHANNEL")
        reports = self.query_set.filter(create_at__gte=(date.today() - timedelta(days=7)), report_type="REPORT_CHANNEL")
        serializer = self.serializer_class(reports, many=True)
        allReportedChannelsSerializer = self.serializer_class(allReportedChannels, many=True)
        percentage = 0
        if len(allReportedChannelsSerializer.data) > 0:
            percentage = float(format(len(serializer.data) / len(allReportedChannels.data), ".4f"))
        return Response({"message": "Get recent reported channels successfully", "data": {
            'data': serializer.data,
            "percentage": percentage
        }})
    
    def getRecentAllReports(self, request):
        allReports = self.query_set.all()
        reports = self.query_set.filter(create_at__gte=(date.today() - timedelta(days=7)))
        serializer = self.serializer_class(reports, many=True)
        allReportsSerializer = self.serializer_class(allReports, many=True)
        percentage = 0
        if len(allReportsSerializer.data) > 0:
            percentage = float(format(len(serializer.data) / len(allReportsSerializer.data), ".4f"))
        return Response({"message": "Get recent all reports successfully", "data": {
            "data": serializer.data,
            "percentage": percentage
        }})

    def getAllReportsStat(self, request):
        reportedUsers = self.query_set.filter(report_type="REPORT_USER")
        reportedChannels = self.query_set.filter(report_type="REPORT_CHANNEL")
        reportedUsersSerializer = self.serializer_class(reportedUsers, many=True)
        reportedChannelsSerializer = self.serializer_class(reportedChannels, many=True)
        return Response({"message": "Get stat of all reports successfully", "data": {
            "reported_users": len(reportedUsersSerializer.data),
            "reported_channels": len(reportedChannelsSerializer.data)
        }})
        
    def getRecentAllReportsStat(self, request):
        totalReportedUsers = self.query_set.filter(report_type="REPORT_USER")
        totalReportedChannels = self.query_set.filter(report_type="REPORT_CHANNEL")
        totalReportedUsersSerializer = self.serializer_class(totalReportedUsers, many=True)
        totalReportedChannelsSerializer = self.serializer_class(totalReportedChannels, many=True)
        reportedUsers = self.query_set.filter(create_at__gte=(date.today() - timedelta(days=7)), report_type="REPORT_USER")
        reportedChannels = self.query_set.filter(create_at__gte=(date.today() - timedelta(days=7)), report_type="REPORT_CHANNEL")
        reportedUsersSerializer = self.serializer_class(reportedUsers, many=True)
        reportedChannelsSerializer = self.serializer_class(reportedChannels, many=True)
        userPercentage = 0
        channelPercentage = 0
        if len(totalReportedUsersSerializer.data) > 0:
            userPercentage = float(format(len(reportedUsersSerializer.data) / len(totalReportedUsersSerializer.data), ".4f"))
        if len(totalReportedChannelsSerializer.data) > 0:
            channelPercentage = float(format(len(reportedChannelsSerializer.data) / len(totalReportedChannelsSerializer.data), ".4f"))
        return Response({"message": "Get stat of all reports successfully", "data": {
            "reported_users": {
                "number": len(reportedUsersSerializer.data),
                "percentage": userPercentage
            },
            "reported_channels": {
                "number": len(reportedChannelsSerializer.data),
                "percentage": channelPercentage
            }
        }})
    @createReportSchema
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


    @getReportDetailSchema
    def getReportDetail(self, request, reportId):
        try:
            report = self.query_set.get(pk=reportId)
            serializer = self.serializer_class(report, many=False)
            return Response({"message": "Get report detail successfully", "data": serializer.data})
        except:
            return Response({"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

    @processReportSchema
    def processReport(self, request, reportId):
        try:
            report = self.query_set.get(pk=reportId)
            report.processed = True
            report.save()
            return Response({"message": "Process report successfully"})
        except:
            return Response({"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

    @deleteReportSchema
    def deleteReport(self, request, reportId):
        try:
            report = self.query_set.get(pk=reportId)
            report.delete()
            return Response({"message": "Delete report successfully"})
        except:
            return Response({"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)