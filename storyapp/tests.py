import datetime
from django.test import TestCase
from pytz import UTC

from storyapp.models import Story, Scene

class StoryTestCase(TestCase):
    def setUp(self):
        story = Story.objects.create(
            title="The Crucible",
            draft_raw='{"blocks":[{"key":"2mr2t","text":"***adv1jxgj***\\n\\nbang!","type":"unstyled","depth":0,'
                      '"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":16,"key":0}],"data":{}},'
                      '{"key":"q9lk","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],'
                      '"data":{}},{"key":"77mcv","text":"***iwts6fnh***\\n\\nwhisper","type":"unstyled","depth":0,'
                      '"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":16,"key":1}],"data":{}}],'
                      '"entityMap":{"0":{"type":"SCENE","mutability":"IMMUTABLE","data":"adv1jxgj"},'
                      '"1":{"type":"SCENE","mutability":"IMMUTABLE","data":"iwts6fnh"}}}',
            last_updated=datetime.datetime(2021, 2, 10, 0, 57, 43, 899746, tzinfo=datetime.timezone.utc)
        )
        Scene.objects.create(
            entity_key="adv1jxgj",
            content_blocks="",
            card_summary="An exciting intro",
            location=None,
            story=story
        )
        Scene.objects.create(
            entity_key="iwts6fnh",
            content_blocks="",
            card_summary="a thrilling conclusion",
            location=None,
            story=story
        )

    def test_scene_set(self):
        """story can find all scenes belonging to it with scene_set"""
        story = Story.objects.get(title="The Crucible")
        story_scenes = story.scene_set()
        scene_one = Scene.objects.get(entity_key="adv1jxgj")
        scene_two = Scene.objects.get(entity_key="iwts6fnh")

        self.assertEqual(len(story_scenes), 2)
        self.assertIn(scene_one, story_scenes)
        self.assertIn(scene_two, story_scenes)

    def test_split_text(self):
        """split_text saves each scene's story content to that scene's object"""
        story = Story.objects.get(title="The Crucible")
        scene_one = Scene.objects.get(entity_key="adv1jxgj")
        scene_two = Scene.objects.get(entity_key="iwts6fnh")
        story.split_text()
        scene_one_count=len(Scene.objects.filter(entity_key="adv1jxgj"))

        expected_scene_one = '[{"key":"2mr2t","text":"***adv1jxgj***\n\nbang!","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":16,"key":0}],"data":{}},{"key":"q9lk","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]'
        expected_scene_two = '[{"key":"77mcv","text":"***iwts6fnh***\n\nwhisper","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":16,"key":1}],"data":{}}]'

        # self.assertEqual(scene_one.content_blocks, expected_scene_one)
        # self.assertEqual(scene_two.content_blocks, expected_scene_two)
        self.assertEqual(scene_one.location, 1)
        self.assertEqual(scene_two.location, 2)
        self.assertEqual(scene_one_count, 1)