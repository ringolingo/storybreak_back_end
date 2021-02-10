from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import StorySerializer, SceneSerializer
from .models import Story, Scene


class StoryView(viewsets.ViewSet):
    def list(self, request):
        queryset = Story.objects.all()
        serializer = StorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Story.objects.all()
        story = get_object_or_404(queryset, pk=pk)
        serializer = StorySerializer(story)
        return Response(serializer.data)

    def create(self, request):
        serializer = StorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"success", "data":serializer.data})

    def update(self, request, pk=None):
        try:
            story = Story.objects.get(id=pk)
            serializer = StorySerializer(story, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except:
            return Response({"message":"invalid story or request"})
        return Response({"message":"successful", "data":serializer.data})

    def destroy(self, request, pk=None):
        queryset = Story.objects.all()
        story = get_object_or_404(queryset, pk=pk)
        serializer = StorySerializer(story, data=request.data)
        serializer.is_valid(raise_exception=True)
        story.delete()
        return Response({"message": "successful", "data":serializer.data})


class SceneView(viewsets.ViewSet):
    def list(self, request):
        if request.query_params:
            story = self.request.query_params.get('story')
            queryset = Scene.objects.filter(story=story)
            serializer = SceneSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = Scene.objects.all()
            serializer = SceneSerializer(queryset, many=True)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Scene.objects.all()
        scene = get_object_or_404(queryset, pk=pk)
        serializer = SceneSerializer(scene)
        return Response(serializer.data)

    def create(self, request):
        serializer = SceneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"success", "data":serializer.data})

    def update(self, request, pk=None):
        try:
            scene = Scene.objects.get(id=pk)
            serializer = SceneSerializer(scene, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except:
            return Response({"message":"invalid scene or request"})
        return Response({"message":"successful", "data":serializer.data})

    def destroy(self, request, pk=None):
        queryset = Scene.objects.all()
        scene = get_object_or_404(queryset, pk=pk)
        serializer = SceneSerializer(scene, data=request.data)
        serializer.is_valid(raise_exception=True)
        scene.delete()
        return Response({"message":"successful", "data":serializer.data})
