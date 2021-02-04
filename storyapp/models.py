from django.db import models

# Create your models here.
class Story(models.Model):
    title = models.CharField(max_length=200)
    draft_raw = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title