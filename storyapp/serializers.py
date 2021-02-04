from rest_framework import serializers
from .models import Story

class StorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Story
    fields = ('title', 'draft_raw', 'last_updated')