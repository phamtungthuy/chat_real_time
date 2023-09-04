from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Message'])
@api_view(['POST'])
def createMessage(request):
    pass

@extend_schema(tags=['Message'])
@api_view(['GET'])
def getAllMessages(request):
    pass

@extend_schema(tags=['Message'])
@api_view(['DELETE'])
def deleteMessage(request, messageId):
    pass
