from django.contrib import admin
from django.urls import path,include
from .views import html_view,CreateRoomAPI,CheckRoomAPI


urlpatterns = [
    path('',html_view,name='html-view'),
    path('lobby/',CreateRoomAPI.as_view(),name='create'),
    path('lobbycheck/',CheckRoomAPI.as_view(),name='join')
]
