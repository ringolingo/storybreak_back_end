from django.contrib import admin
from .models import Story

# Register your models here.
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'draft_raw', 'last_updated')

admin.site.register(Story, StoryAdmin)
