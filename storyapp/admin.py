from django.contrib import admin
from .models import Story, Scene

# Register your models here.
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'draft_raw', 'last_updated')

class SceneAdmin(admin.ModelAdmin):
    list_display = ('entity_key', 'content_blocks', 'card_summary', 'location', 'id', 'story')

admin.site.register(Story, StoryAdmin)
admin.site.register(Scene, SceneAdmin)