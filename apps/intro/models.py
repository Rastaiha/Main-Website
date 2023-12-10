from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class HomepageData(models.Model):
    intro = RichTextUploadingField()
    video_url = models.URLField(null=True, blank=True)


class UpcomingEvent(models.Model):
    poster = models.ImageField(null=False, blank=False)
    intro = RichTextUploadingField()
    title = models.CharField(max_length=100, null=False, blank=False)
    button_link = models.URLField(null=False, blank=False)
    button_name = models.CharField(null=False, blank=False, max_length=50)
    show_on_homepage = models.BooleanField(
        default=True, null=False, blank=False)

    def __str__(self):
        return self.title
