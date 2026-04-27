from django.db import models


class Media(models.Model):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'

    MEDIA_TYPE_CHOICES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (AUDIO, 'Audio'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
