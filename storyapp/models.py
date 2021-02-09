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

    # TODO checking on how well (if at all) this works is going to require having
    # scenes that are actually tied to the text
    # update IT SEEMS LIKE THIS WORKS? TENTATIVELY? WHEN THERE ARE ACTUAL SCENE OBJECTS IN THE TEXT?
    def chunk_text(self):
        # reset all scene locations so they can be updated based on text
        # and any removed from text will then be removed from location-based lineup
        scenes = self.scene_set()
        for scene in scenes:
            scene.location = None

        # parse full content into scenes by finding blocks that are entities
        # and grouping subsequent blocks with them until finding next entity
        raw = json.loads(self.draft_raw)
        holder = []
        index = None
        entity_key = ''

        for block in raw['blocks']:
            # if current block is a scene break and there's content in the holder,
            # we want to save that content to it's appropriate scene object
            if len(block['entityRanges']) > 0 and len(holder) > 0:
                scene = Scene.objects.get(entity_key=entity_key)
                scene.content_blocks = json.dumps(holder, separators=(',', ':'))
                scene.location = index
                # save the related line in entityMap into the scene? as a new scene property maybe?
                scene.save()
                holder = []

            if len(block['entityRanges']) > 0:
                index = block['entityRanges'][0]['key']
                entity_key = raw['entityMap'][str(index)]['data']
                holder.append(block)
            else:
                holder.append(block)
        else:
            scene = Scene.objects.get(entity_key=entity_key)
            scene.content_blocks = json.dumps(holder, separators=(',', ':'))
            scene.location = index
            # save the related line in entityMap into the scene? as a new scene property maybe?
            scene.save()


    # def assemble_text(self):
    #   start by json loading draft_raw and setting raw['blocks'] = [] and raw['entityMap'] = {}
    # have to build 'blocks' and 'entitymap'

    # building blocks:
    # each through scenes
    # shove the contents of scene.content_blocks into blocks
    # make sure not nesting arrays in arrays
    # (maybe do raw['blocks'].append(...scene.content_blocks) - does python have a spread operator?
    # or do a further nested each look, pushing the content blocks into blocks one at a time

    # building entitymap:
    # entityMap is really just the same one object with the 'immutable, scene' blah blah
    # and the differences are the keys and the data
    # so like each through scene_set - for each scene, add to the entitymap object
    # a key of scene.location and a value of that one same object as always with data set to scene.entity_key

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
