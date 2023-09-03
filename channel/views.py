from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def createChannel(request):
    pass

@api_view(['GET'])
def getAllChannels(request):
    pass

@api_view(['PUT'])
def updateChannel(request):
    pass

@api_view(['DELETE'])
def deleteChannel(request, id):
    pass
