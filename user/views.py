from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
# from .serializers import *
from djoser.serializers import UserSerializer
import requests
# Create your views here.

class verifyAPI(APIView):
    def get(self,request,uid,token):
        activation_url = "http://127.0.0.1:8000/auth/users/activation/"

        data = {
            "uid": uid,
            "token": token,
        }

        response = requests.post(activation_url, data=data)

        if response.status_code == 204:
            return Response(
                {"message":"Account activated successfully."}
            )
        else:
            return Response(
                {"error":{"detail":f"Invalid link or account already verified"}}
            )