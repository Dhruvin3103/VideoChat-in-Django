from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import LobbySerializer
from .models import Lobby
# Create your views here.

def html_view(request):
    context ={}

    return render(request,'main.html',context=context)

class CreateRoomAPI(GenericAPIView):
    serializer_class = LobbySerializer
    queryset = Lobby.objects.all()
    
    def post(self,request):
        try:
            self.create(request)
        except Exception as e:
            return Response({
                'status': 403,
                'error' : e
            })

