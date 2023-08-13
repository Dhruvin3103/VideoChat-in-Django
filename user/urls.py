from django.urls import path,include
from .views import verifyAPI
urlpatterns = [
    path('activate/<uid>/<token>/',verifyAPI.as_view()),
]
