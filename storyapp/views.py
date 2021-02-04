from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StorySerializer
from .models import Story

class StoryView(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    queryset = Story.objects.all()
