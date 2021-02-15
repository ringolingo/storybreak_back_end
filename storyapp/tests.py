import datetime
import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

from storyapp.models import Story, Scene, User
from .serializers import StorySerializer

client = Client()


class StoryTestCase(TestCase):
    def setUp(self):
        self.ringo = User.objects.create(
            email="ringo@fake.com",
            first_name="Ringo",
            last_name="Starr"
        )

        self.george = User.objects.create(
            email="george@fake.com",
            first_name="George",
            last_name="Harrison"
        )

        story = Story.objects.create(
            title="The Crucible",
            draft_raw='{"blocks":[{"key":"92eck","text":"***dr2hgl5j***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}},{"key":"9e0ci","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bdih4","text":"a new line of text, mmm","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bbser","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"9bit5","text":"***milhz12y***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":1}],"data":{}},{"key":"4kf5f","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"dgvci","text":"bloop","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{"0":{"type":"SCENE","mutability":"IMMUTABLE","data":"dr2hgl5j"},"1":{"type":"SCENE","mutability":"IMMUTABLE","data":"milhz12y"}}}',
            last_updated=datetime.datetime(2021, 2, 10, 0, 57, 43, 899746, tzinfo=datetime.timezone.utc),
            user=self.ringo
        )
        Scene.objects.create(
            entity_key="dr2hgl5j",
            content_blocks="",
            card_summary="An exciting intro",
            location=3,
            story=story
        )
        Scene.objects.create(
            entity_key="milhz12y",
            content_blocks="",
            card_summary="a thrilling conclusion",
            location=4,
            story=story
        )
        Scene.objects.create(
            entity_key="b1d6j7aa",
            content_blocks='{"key":"1mr2t","text":"I have a None location and do not belong in the scene_set*","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}}',
            card_summary="a villain appears",
            location=None,
            story=story
        )
        Scene.objects.create(
            entity_key="als930sk",
            content_blocks='{"key":"1mr2t","text":"I start with a location but it should be set to None by the end of this*","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}}',
            card_summary="more villains",
            location=1,
            story=story
        )


        story_two = Story.objects.create(
            title="Vindication",
            draft_raw='{"blocks":["I better not show up in any test results"],"entityMap":{"0":"me neither"}}',
            last_updated=datetime.datetime(2021, 2, 10, 0, 57, 43, 899746, tzinfo=datetime.timezone.utc),
            user=self.ringo
        )
        Scene.objects.create(
            entity_key="x2m2c5kd",
            content_blocks='[{"key":"1ch14","text":"***x2m2c5kd***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":1}],"data":{}},{"key":"1a2m9","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"ed3om","text":"whimper","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"f64jc","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]',
            card_summary="avengers unassemble",
            location=1,
            story=story_two
        )
        Scene.objects.create(
            entity_key="ymcm8tfx",
            content_blocks='[{"key":"2mr2t","text":"***ymcm8tfx***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}},{"key":"3ngqt","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"ffhk","text":"bang","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"13mb0","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]',
            card_summary="avengers assemble",
            location=0,
            story=story_two
        )
        Scene.objects.create(
            entity_key="badbadug",
            content_blocks='{"key":"1mr2t","text":"I am a repeat with a None location and do not belong in the final product*","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}}',
            card_summary="a villain appears",
            location=None,
            story=story_two
        )


        story_with_deleted_scene = Story.objects.create(
            title="Alas",
            user=self.george,
            draft_raw='{"blocks":[{"key":"4fdnc","text":"***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":3,"key":0}],"data":{}},{"key":"3ov3t","text":"one","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"9l94n","text":"***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":3,"key":1}],"data":{}},{"key":"867gh","text":"two","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"fje60","text":"***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":3,"key":2}],"data":{}},{"key":"224hb","text":"three","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{"0":{"type":"SCENE","mutability":"IMMUTABLE","data":"61ifpubi"},"1":{"type":"SCENE","mutability":"IMMUTABLE","data":"ux72sqf2"},"2":{"type":"SCENE","mutability":"IMMUTABLE","data":"5i35elhw"}}}'
        )
        Scene.objects.create(
            entity_key='ux72sqf2',
            card_summary='2',
            location=0,
            story=story_with_deleted_scene,
            content_blocks='[{"key":"9l94n","text":"***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":3,"key":1}],"data":{}},{"key":"867gh","text":"two","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]'
        )
        Scene.objects.create(
            entity_key='5i35elhw',
            card_summary='3',
            location=1,
            story=story_with_deleted_scene,
            content_blocks='[{"key":"fje60","text":"***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":3,"key":2}],"data":{}},{"key":"224hb","text":"three","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]'
        )


    def test_scene_set(self):
        """story can find all scenes belonging to it with scene_set"""
        story = Story.objects.get(title="The Crucible")
        story_scenes = story.scene_set()
        scene_one = Scene.objects.get(entity_key="dr2hgl5j")
        scene_two = Scene.objects.get(entity_key="milhz12y")
        scene_three = Scene.objects.get(entity_key="b1d6j7aa")
        scene_four = Scene.objects.get(entity_key="als930sk")

        self.assertEqual(len(story_scenes), 3)
        self.assertIn(scene_one, story_scenes)
        self.assertIn(scene_two, story_scenes)
        self.assertNotIn(scene_three, story_scenes)
        self.assertIn(scene_four, story_scenes)

    def test_split_text(self):
        """split_text saves each scene's story content to that scene's object"""
        story = Story.objects.get(title="The Crucible")
        story.split_text()

        scene_one = Scene.objects.get(entity_key="dr2hgl5j")
        scene_two = Scene.objects.get(entity_key="milhz12y")
        scene_four = Scene.objects.get(entity_key="als930sk")

        expected_scene_one = '[{"key":"92eck","text":"***dr2hgl5j***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}},{"key":"9e0ci","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bdih4","text":"a new line of text, mmm","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bbser","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]'
        expected_scene_two = '[{"key":"9bit5","text":"***milhz12y***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":1}],"data":{}},{"key":"4kf5f","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"dgvci","text":"bloop","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]'

        self.assertEqual(scene_one.content_blocks, expected_scene_one)
        self.assertEqual(scene_two.content_blocks, expected_scene_two)
        self.assertEqual(scene_one.location, 0)
        self.assertEqual(scene_two.location, 1)
        self.assertEqual(scene_four.location, None)

    def test_assemble_text(self):
        """assemble_text creates a new draft_raw for the story based on that story's scenes' content_blocks"""
        story = Story.objects.get(title="Vindication")
        story.assemble_text()

        expected_story_draft_raw = '{"blocks":[{"key":"2mr2t","text":"***ymcm8tfx***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}},{"key":"3ngqt","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"ffhk","text":"bang","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"13mb0","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"1ch14","text":"***x2m2c5kd***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":1}],"data":{}},{"key":"1a2m9","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"ed3om","text":"whimper","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"f64jc","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{"0":{"type":"SCENE","mutability":"IMMUTABLE","data":"ymcm8tfx"},"1":{"type":"SCENE","mutability":"IMMUTABLE","data":"x2m2c5kd"}}}'
        self.assertEqual(expected_story_draft_raw, story.draft_raw)

    def test_assemble_text_with_deleted_scene(self):
        """assemble_text creates a new draft_raw for a story after a scene from that story was deleted"""
        story = Story.objects.get(title="Alas")
        story.assemble_text()

        expected_story_draft_raw = '{"blocks":[{"key":"9l94n","text":"***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":3,"key":0}],"data":{}},{"key":"867gh","text":"two","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"fje60","text":"***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":3,"key":1}],"data":{}},{"key":"224hb","text":"three","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{"0":{"type":"SCENE","mutability":"IMMUTABLE","data":"ux72sqf2"},"1":{"type":"SCENE","mutability":"IMMUTABLE","data":"5i35elhw"}}}'
        self.assertEqual(expected_story_draft_raw, story.draft_raw)

    def test_save(self):
        """saving the story causes the cards to update, so they match most the current user work"""
        story = Story.objects.get(title="The Crucible")
        story.save()

        scene_one = Scene.objects.get(entity_key="dr2hgl5j")
        scene_two = Scene.objects.get(entity_key="milhz12y")
        scene_four = Scene.objects.get(entity_key="als930sk")

        expected_scene_one = '[{"key":"92eck","text":"***dr2hgl5j***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}},{"key":"9e0ci","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bdih4","text":"a new line of text, mmm","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bbser","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]'
        expected_scene_two = '[{"key":"9bit5","text":"***milhz12y***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":1}],"data":{}},{"key":"4kf5f","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"dgvci","text":"bloop","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]'

        self.assertEqual(scene_one.content_blocks, expected_scene_one)
        self.assertEqual(scene_two.content_blocks, expected_scene_two)
        self.assertEqual(scene_one.location, 0)
        self.assertEqual(scene_two.location, 1)
        self.assertEqual(scene_four.location, None)


class StorySerializerTestCase(TestCase):
    def setUp(self):
        self.ringo = User.objects.create(
            email="ringo@fake.com",
            first_name="Ringo",
            last_name="Starr"
        )

        self.george = User.objects.create(
            email="george@fake.com",
            first_name="George",
            last_name="Harrison"
        )

        self.story = Story.objects.create(
            title="The Crucible",
            user=self.ringo,
            draft_raw='{"blocks":[{"key":"92eck","text":"***dr2hgl5j***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}},{"key":"9e0ci","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bdih4","text":"a new line of text, mmm","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bbser","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"9bit5","text":"***milhz12y***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":1}],"data":{}},{"key":"4kf5f","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"dgvci","text":"bloop","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{"0":{"type":"SCENE","mutability":"IMMUTABLE","data":"dr2hgl5j"},"1":{"type":"SCENE","mutability":"IMMUTABLE","data":"milhz12y"}}}',
        )
        self.crucible_scene_one = Scene.objects.create(
            entity_key="dr2hgl5j",
            content_blocks="",
            card_summary="An exciting intro",
            location=3,
            story=self.story
        )
        self.crucible_scene_two = Scene.objects.create(
            entity_key="milhz12y",
            content_blocks="",
            card_summary="a thrilling conclusion",
            location=4,
            story=self.story
        )
        self.crucible_scene_three = Scene.objects.create(
            entity_key="b1d6j7aa",
            content_blocks='{"key":"1mr2t","text":"I have a None location and do not belong in the scene_set*","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}}',
            card_summary="a villain appears",
            location=None,
            story=self.story
        )
        self.crucible_scene_four = Scene.objects.create(
            entity_key="als930sk",
            content_blocks='{"key":"1mr2t","text":"I start with a location but it should be set to None by the end of this*","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}}',
            card_summary="more villains",
            location=1,
            story=self.story
        )

        self.story_two = Story.objects.create(
            title="Vindication",
            user=self.george,
            draft_raw='{"blocks":["I better not show up in any test results"],"entityMap":{"0":"me neither"}}',
            last_updated=datetime.datetime(2021, 2, 10, 0, 57, 43, 899746, tzinfo=datetime.timezone.utc)
        )
        self.vindication_scene_one = Scene.objects.create(
            entity_key="x2m2c5kd",
            content_blocks='[{"key":"1ch14","text":"***x2m2c5kd***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":1}],"data":{}},{"key":"1a2m9","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"ed3om","text":"whimper","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"f64jc","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]',
            card_summary="avengers unassemble",
            location=1,
            story=self.story_two
        )
        self.vindication_scene_two = Scene.objects.create(
            entity_key="ymcm8tfx",
            content_blocks='[{"key":"2mr2t","text":"***ymcm8tfx***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}},{"key":"3ngqt","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"ffhk","text":"bang","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"13mb0","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]',
            card_summary="avengers assemble",
            location=0,
            story=self.story_two
        )
        self.vindication_scene_three = Scene.objects.create(
            entity_key="badbadug",
            content_blocks='{"key":"1mr2t","text":"I am a repeat with a None location and do not belong in the final product*","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}}',
            card_summary="a villain appears",
            location=None,
            story=self.story_two
        )

        self.valid_new_story = {
            "title": "Cromulent",
            "user": 1,
            "draft_raw":'{"blocks":[{"key":"alskd","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"do6","text":"***y07hjbh4***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}},{"key":"e0c25","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bria5","text":"ah yes, it was spring","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"elbs7","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"du9qf","text":"and the smell of fresh tar was everywhere","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"81es1","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"8u06p","text":"\\"this was extremely funny, thanks,\\" the protagonist said.","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{"0":{"type":"SCENE","mutability":"IMMUTABLE","data":"y07hjbh4"}}}'
        }

        self.invalid_new_story = {
            "title": "",
            "draft_raw": "okay and now when the story ISN'T good you DON'T have a problem, I see how it is"
        }

    def test_get_all_stories(self):
        """get can retrieve all stories"""
        id = self.ringo.id
        response = client.get(reverse('story-list'))
        stories = Story.objects.filter(title="The Crucible")
        serializer = StorySerializer(stories, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_valid_story(self):
        """get can retrieve a story with the given pk
        get updates the story's draft_raw based on its cards before returning to user"""
        response = client.get(reverse('story-detail', kwargs={'pk': self.story_two.id}))
        story = Story.objects.get(id=self.story_two.id)
        serializer = StorySerializer(story)

        expected_story_draft_raw = '{"blocks":[{"key":"2mr2t","text":"***ymcm8tfx***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}},{"key":"3ngqt","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"ffhk","text":"bang","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"13mb0","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"1ch14","text":"***x2m2c5kd***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":1}],"data":{}},{"key":"1a2m9","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"ed3om","text":"whimper","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"f64jc","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{"0":{"type":"SCENE","mutability":"IMMUTABLE","data":"ymcm8tfx"},"1":{"type":"SCENE","mutability":"IMMUTABLE","data":"x2m2c5kd"}}}'

        self.assertEqual(response.data['draft_raw'], serializer.data['draft_raw'])
        self.assertEqual(expected_story_draft_raw, response.data["draft_raw"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_invalid_story(self):
        """get returns 404 if no such story"""
        response = client.get(reverse('story-detail', kwargs={'pk': 38}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_story(self):
        """create can create a story and save it in database
        saves it with the draft_raw as it just received from the story
        draft_raw has not been affected by the scene objects"""
        response = client.post(reverse('story-list'), data=self.valid_new_story)
        expected_draft_raw = '{"blocks":[{"key":"alskd","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"do6","text":"***y07hjbh4***","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":14,"key":0}],"data":{}},{"key":"e0c25","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bria5","text":"ah yes, it was spring","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"elbs7","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"du9qf","text":"and the smell of fresh tar was everywhere","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"81es1","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"8u06p","text":"\\"this was extremely funny, thanks,\\" the protagonist said.","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{"0":{"type":"SCENE","mutability":"IMMUTABLE","data":"y07hjbh4"}}}'

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['draft_raw'], expected_draft_raw)

    def test_create_invalid_story(self):
        """create does not save a story with bad data"""
        response = client.post(reverse('story-list'), data=self.invalid_new_story)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_story(self):
        """update can update story with the given pk
        after update, the database has the story draft_raw as it was just sent
        -- has not changed it based on scene objects"""
        updated_story = {"title": "I'd loooove for this to work", "draft_raw": self.story.draft_raw}
        response = client.put(reverse('story-detail', kwargs={'pk': self.story.id}), data=json.dumps(updated_story), content_type='application/json')

        self.assertEqual(response.data['draft_raw'], updated_story['draft_raw'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_story(self):
        """update does not save story if data is bad"""
        response = client.put(reverse('story-detail', kwargs={'pk': self.story.id}), data=json.dumps(self.invalid_new_story), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_story(self):
        """delete correctly deletes story"""
        response = client.delete(reverse('story-detail', kwargs={'pk': self.story.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_story(self):
        """delete returns 404 if story not found"""
        response = client.delete(reverse('story-detail', kwargs={'pk': 38}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
