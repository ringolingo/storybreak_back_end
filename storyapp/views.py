from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import StorySerializer, SceneSerializer
from .models import Story, Scene
from django.views.generic.list import ListView


class StoryView(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    queryset = Story.objects.all()

class SceneView(viewsets.ModelViewSet):
    serializer_class = SceneSerializer
    queryset = Scene.objects.all()

    # Scene.objects.filter(story__in=Story.objects.filter(id=id))
    # Child.objects.filter(parent__in=Parent.objects.filter(name__startswith='A'))
    # def get_queryset(self):
    #     queryset = Scene.objects.all()
    #     story = self.request.query_params.get('story')
    #     queryset = queryset.filter(story=story)
    #     return queryset

    # this doesn't work
    # Object of type Scene is not JSON serializable
    # def list(self, request):
    #     story = self.request.query_params.get('story')
    #     results = Scene.objects.filter(story=story)
    #     return Response(results)

    # or this
    # AttributeError when attempting to get a value for field `entity_key` on serializer `SceneSerializer`.
    # def list(self, request):
    #     story = self.request.query_params.get('story')
    #     result = Scene.objects.filter(story=story)
    #     serializer = SceneSerializer(result, many=False)
    #     return Response(serializer.data)
