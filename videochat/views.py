from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,ListAPIView
from .serializers import LobbySerializer
from .models import Lobby
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Create your views here.

def html_view(request):
    context ={}

    return render(request,'main.html',context=context)

class CreateRoomAPI(GenericAPIView):
    serializer_class = LobbySerializer
    # permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            serializer = LobbySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':200,
                    'message':'Go ahead',
                    'data':serializer.data
                })
            else:
                return Response({
                    'status': 400,
                    'errors': serializer.errors  # Use 'errors' key for the validation errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 403,
                'error': str(e)
            }, status=status.HTTP_403_FORBIDDEN)

class CheckRoomAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self,request):
        lobby_code = request.data['lobby_id']
        # lobby_code = "home"
        lobby = Lobby.objects.filter(lobby_id=lobby_code).first()
        
        try:
            if lobby:
                return Response({
                    'status':200,
                    'message':'Go ahead'
                })
            else:
                return Response({
                    'status':404,
                    'error':"Lobby couldnt found check the code again"
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status':400,
                'exception':str(e)
            }, status=status.HTTP_403_FORBIDDEN)
