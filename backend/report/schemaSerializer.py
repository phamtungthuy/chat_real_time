from rest_framework import serializers
from .serializer import *
class GeneralMessageSerializer(serializers.Serializer):
    message = serializers.CharField()

class SuccessGetReportedChannelSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ReportSerializer(many=True)

class SuccessGetReportedUserSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ReportSerializer(many=True)

class SuccessCreateReportSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ReportSerializer()

class SuccessGetReportDetailSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ReportSerializer(many=True)