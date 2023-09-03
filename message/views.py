from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def createMessage(request):
    pass

@api_view(['GET'])
def getAllMessages(request):
    pass

@api_view(['DELETE'])
def deleteMessage(request, messageId):
    pass
