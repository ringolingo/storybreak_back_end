from rest_framework import serializers
from .models import Story, Scene


# class StorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Story
#         fields = ('title', 'draft_raw', 'last_updated', 'id')
#
# class SceneSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Scene
#         fields = ('entity_key', 'content_blocks', 'card_summary', 'location', 'id', 'story')

class SceneSerializer(serializers.HyperlinkedModelSerializer):
    story_id = serializers.PrimaryKeyRelatedField(queryset=Story.objects.all(), source='story.id')

    class Meta:
        model = Scene
        fields = ('entity_key', 'content_blocks', 'card_summary', 'location', 'id', 'story_id')

    def create(self, validated_data):
        scene = Scene.objects.create(story=validated_data['story']['id'], scene=validated_data['entity_key'])
        return scene


class StorySerializer(serializers.HyperlinkedModelSerializer):
    scenes = SceneSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = ('title', 'draft_raw', 'last_updated', 'id', 'scenes')
