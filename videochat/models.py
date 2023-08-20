from django.db import models
from user.models import User
# Create your models here.
class Lobby(models.Model):
    lobby_id = models.CharField('lobby id', max_length=20, unique=True)
    lobby_users = models.ManyToManyField(User,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.lobby_id)