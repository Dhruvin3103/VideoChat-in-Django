from django.contrib import admin
from django.urls import path,include
from .views import html_view


urlpatterns = [
    path('',html_view,name='html-view')
]
