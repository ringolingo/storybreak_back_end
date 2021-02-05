from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StorySerializer, SceneSerializer
from .models import Story, Scene

class StoryView(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    queryset = Story.objects.all()

class SceneView(viewsets.ModelViewSet):
    serializer_class = SceneSerializer
    queryset = Scene.objects.all()
