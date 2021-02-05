from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import StorySerializer, SceneSerializer
from .models import Story, Scene
from django.views.generic.list import ListView


class StoryView(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    queryset = Story.objects.all()

class SceneView(viewsets.ModelViewSet):
    serializer_class = SceneSerializer
    queryset = Scene.objects.all()

    # def get_object(self):
    #     queryset = Scene.objects.all()
    #     id = self.request.query_params.get('id')
    #     scene = queryset.get(id=id)
    #     return scene

    # def get_object(self):
    #       ??????
