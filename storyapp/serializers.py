from rest_framework import serializers
from .models import Story, Scene

class StorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Story
    fields = ('title', 'draft_raw', 'last_updated', 'id')

class SceneSerializer(serializers.ModelSerializer):
  story_id = serializers.IntegerField(read_only=True, source="story.id")

  class Meta:
    model = Scene
    fields = ('entity_key', 'content_blocks', 'card_summary', 'location', 'id', 'story_id')
