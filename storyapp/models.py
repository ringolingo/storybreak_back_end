from django.db import models
import json

class Story(models.Model):
    title = models.CharField(max_length=200)
    draft_raw = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='stories')

    class Meta:
        ordering = ('-last_updated', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # when story is saved, it updates its scenes accordingly
        self.split_text()
        super().save(*args, **kwargs)

    def scene_set(self):
        # returns scenes that belong to this story and are active (have a location)
        return Scene.objects.filter(location__isnull=False, story=self)

    def split_text(self):
        # does not run when story is first being created (has no text)
        if not self.id:
            return

        # reset all scene locations so only the ones in most recent text update will be part of scene_set
        scenes = self.scene_set()
        for scene in scenes:
            scene.location = None
            scene.save()

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
            # if the current block is a new scene break, and we need to save the last scene's content before moving on
            elif len(block['entityRanges']) > 0:
                try:
                    scene = Scene.objects.get(entity_key=break_id)
                    scene.content_blocks = json.dumps(holder, separators=(',', ':'))
                    scene.location = index
                    scene.save()
                except:
                    pass

                holder = []
                index = block['entityRanges'][0]['key']
                break_id = raw['entityMap'][str(index)]['data']
                holder.append(block)
            # if the current block is just an ordinary non-scene-break line
            else:
                holder.append(block)
        else:
            try:
                scene = Scene.objects.get(entity_key=break_id)
                scene.content_blocks = json.dumps(holder, separators=(',', ':'))
                scene.location = index
                scene.save()
            except:
                pass

    # when the story is retrieved, its draft_raw is updated to be in line with the last saved scenes
    def assemble_text(self):
        # clearout whatever story.draft_raw currently has
        raw_json = json.loads(self.draft_raw)
        raw_json['blocks'] = []
        raw_json['entityMap'] = {}

        # gather all the scenes that are active (have location values)
        active_scenes = self.scene_set()
        for scene in active_scenes:
            # load the scene's content blocks and add to story's draft_raw
            content = json.loads(scene.content_blocks)
            content[0]['entityRanges'][0]['key'] = scene.location
            raw_json['blocks'] += content

            # assemble entity map, adding a new dict for each scene and giving it the appropriate data value
            # entity_map_value: {'type': 'SCENE', 'mutability': 'IMMUTABLE', 'data': __________ }
            raw_json['entityMap'][str(scene.location)] = {'type': 'SCENE', 'mutability': 'IMMUTABLE', 'data': scene.entity_key}

        # take now-current draft_raw and turn it back into a messy string
        updated_content = json.dumps(raw_json, separators=(',',':'))
        self.draft_raw = updated_content
        self.save()
        # return draft_raw value for use in StoryRetrieveSerializer
        # return updated_content


class Scene(models.Model):
    entity_key = models.CharField(max_length=8, blank=True)
    content_blocks = models.TextField(blank=True)
    card_summary = models.TextField(blank=True)
    location = models.IntegerField(null=True)
    story = models.ForeignKey('Story', on_delete=models.CASCADE, related_name='scenes')

    def __str__(self):
        return self.entity_key

    class Meta:
        ordering = ('location', )

class User(models.Model):
    email = models.CharField(max_length=120, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length = 50)
