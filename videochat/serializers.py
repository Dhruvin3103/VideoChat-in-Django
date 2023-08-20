from rest_framework import serializers

from .models import *

class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = '__all__'
