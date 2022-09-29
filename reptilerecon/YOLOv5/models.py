from django.db import models
from django.dispatch import receiver
import os


class Video(models.Model):
    name = models.TextField(max_length=200, default="Sem nome")
    video = models.FileField(upload_to='videos/')
    processed_video = models.FileField(upload_to='processed_videos/', default=None, blank=True, null=True)
    signal = models.FileField(upload_to='signals/', default=None, blank=True, null=True)
    plot = models.FileField(upload_to='plots/', default=None, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)


@receiver(models.signals.post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.video:
        if os.path.isfile(instance.video.path):
            instance.video.delete(save=False)
            instance.processed_video.delete(save=False)
            instance.signal.delete(save=False)
            instance.plot.delete(save=False)
            instance.thumbnail.delete(save=False)
