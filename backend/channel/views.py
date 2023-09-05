from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Channel'])
@api_view(['POST'])
def createChannel(request):
    pass

@extend_schema(tags=['Channel'])
@api_view(['GET'])
def getAllChannels(request):
    pass

@extend_schema(tags=['Channel'])
@api_view(['PUT'])
def updateChannel(request):
    pass

@extend_schema(tags=['Channel'])
@api_view(['DELETE'])
def deleteChannel(request, id):
    pass
