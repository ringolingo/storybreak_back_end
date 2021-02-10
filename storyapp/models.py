from django.db import models
import json

# Create your models here.
class Story(models.Model):
    title = models.CharField(max_length=200)
    draft_raw = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def scene_set(self):
        return Scene.objects.filter(story=self)

    def split_text(self):
        # reset all scene locations so they can be updated based on text
        # and any removed from text will then be removed from location-based lineup
        scenes = self.scene_set()
        for scene in scenes:
            scene.location = None

        # parse full content into scenes by finding blocks that are entities
        # and grouping subsequent blocks with them until finding next entity
        raw = json.loads(self.draft_raw)
        index = None
        break_id = ''
        holder = []

        for block in raw['blocks']:
            # if current block is a scene break and we have no scene content on hold
            if len(block['entityRanges']) > 0 and len(holder) == 0:
                index = block['entityRanges'][0]['key']
                break_id = raw['entityMap'][str(index)]['data']
                holder.append(block)
            elif len(block['entityRanges']) > 0:
                scene = Scene.objects.get(entity_key=break_id)
                scene.content_blocks = json.dumps(holder, separators=(',', ':'))
                scene.location = index
                # save the related line in entityMap into the scene? as a new scene property maybe?
                scene.save()
                holder = []

                index = block['entityRanges'][0]['key']
                break_id = raw['entityMap'][str(index)]['data']
                holder.append(block)
            else:
                holder.append(block)
        else:
            scene = Scene.objects.get(entity_key=break_id)
            scene.content_blocks = json.dumps(holder, separators=(',', ':'))
            scene.location = index
            # save the related line in entityMap into the scene? as a new scene property maybe?
            scene.save()

    def assemble_text(self):
        # steps for assembling story text from scene content blocks:
        # 0. clearout whatever story.draft_raw currently has
        #   start by json loading draft_raw and setting raw['blocks'] = [] and raw['entityMap'] = {}
        raw_json = json.loads(self.draft_raw)
        raw_json['blocks'] = []
        raw_json['entityMap'] = {}
            # I added this bit to check that blocks & entitymap clearing - they do
            # new_string = json.dumps(raw_json)
            # self.draft_raw = new_string
            # self.save()

        # 1. assemble blocks
        # gather all the scenes/filter out ones that don't have location/order by location
        active_scenes = Scene.objects.filter(location__isnull=False, story=self)
        # each through scenes
        for scene in active_scenes:
            # json load the scene's content blocks
            content = json.loads(scene.content_blocks)
            # shove the contents of scene.content_blocks into blocks
            # make sure not nesting arrays in arrays
            raw_json['blocks'] += content

            # 2. assemble entity map
            # entityMap is really just the same one object with the 'immutable, scene' blah blah
            # and the differences are the keys and the data
            # so like each through scene_set - for each scene, add to the entitymap object
            # a key of scene.location and a value of that one same object as always with data set to scene.entity_key
            # entity_map_value: {'type': 'SCENE', 'mutability': 'IMMUTABLE', 'data': __________ }
            raw_json['entityMap'][str(scene.location)] = {'type': 'SCENE', 'mutability': 'IMMUTABLE', 'data': scene.entity_key}

        # having added each scene's content blocks into the draft_raw's 'blocks' array and each scene's break's entity hash to draft_raw's entityMap
        # need to turn perfectly nice data objects back into a messy string
        updated_content = json.dumps(raw_json, separators=(',',':'))
        self.draft_raw = updated_content
        self.save()
        # set draft_raw to messy string
        # save story



class Scene(models.Model):
    entity_key = models.CharField(max_length=8)
    content_blocks = models.TextField(blank=True)
    card_summary = models.TextField(blank=True)
    location = models.IntegerField(null=True)
    story = models.ForeignKey('Story', on_delete=models.CASCADE, related_name='scenes')

    def __str__(self):
        return self.entity_key

    class Meta:
        ordering = ('location', )